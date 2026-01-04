"""
Data Provider Module

Fetches real-time and historical stock data using yfinance and converts it
to StockData objects for use with the screening engine.
"""

import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import asdict

from .core import (
    StockData,
    StockAnalyzer,
    ScreeningEngine,
    ScreeningStrategy,
    ScreeningResult
)


class DataProvider:
    """
    Fetches stock data from Yahoo Finance and converts to StockData objects.
    
    Rules of Thumb Reference (integrated into evaluation):
    - P/E Ratio: 15-20 is reasonable
    - Debt-to-Equity: < 1 is safer
    - Current Ratio: 2:1 is healthy
    - ROE: 15%+ is good
    - Dividend Payout Ratio: < 60% is sustainable
    - P/B Ratio: < 1 may indicate undervaluation
    - Free Cash Flow: Should be positive and growing
    """
    
    def __init__(self):
        """Initialize the DataProvider"""
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
    
    def get_stock_data(self, symbol: str) -> Optional[StockData]:
        """
        Fetch stock data for a single symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            StockData object or None if fetch fails
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get financial statements for more detailed data
            try:
                balance_sheet = ticker.balance_sheet
                income_stmt = ticker.income_stmt
                cash_flow = ticker.cashflow
            except Exception:
                balance_sheet = pd.DataFrame()
                income_stmt = pd.DataFrame()
                cash_flow = pd.DataFrame()
            
            # Extract key metrics with safe defaults
            price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
            eps = info.get('trailingEps', 0) or 0
            market_cap = info.get('marketCap', 0) or 0
            shares_outstanding = info.get('sharesOutstanding', 1) or 1
            
            # Revenue and income
            revenue = info.get('totalRevenue', 0) or 0
            net_income = info.get('netIncomeToCommon', 0) or 0
            
            # Balance sheet items
            total_assets = info.get('totalAssets', 0) or 0
            total_liabilities = info.get('totalLiab', 0) or info.get('totalDebt', 0) or 0
            cash = info.get('totalCash', 0) or 0
            debt = info.get('totalDebt', 0) or 0
            
            # Book value
            book_value = info.get('bookValue', 0) or 0
            
            # Growth metrics
            revenue_growth = (info.get('revenueGrowth', 0) or 0) * 100  # Convert to percentage
            earnings_growth = (info.get('earningsGrowth', 0) or 0) * 100
            
            # Dividend info
            dividend_rate = info.get('dividendRate', 0) or 0
            dividend_yield = (info.get('dividendYield', 0) or 0) * 100  # Convert to percentage
            
            # Pre-calculated ratios from yfinance
            pe_ratio = info.get('trailingPE')
            pb_ratio = info.get('priceToBook')
            peg_ratio = info.get('pegRatio')
            roe = (info.get('returnOnEquity', 0) or 0) * 100
            roa = (info.get('returnOnAssets', 0) or 0) * 100
            debt_to_equity = info.get('debtToEquity', 0) or 0
            current_ratio = info.get('currentRatio')
            quick_ratio = info.get('quickRatio')
            
            stock_data = StockData(
                symbol=symbol.upper(),
                price=price,
                eps=eps,
                revenue=revenue,
                net_income=net_income,
                total_assets=total_assets,
                total_liabilities=total_liabilities,
                cash=cash,
                debt=debt,
                shares_outstanding=shares_outstanding,
                market_cap=market_cap,
                dividend_per_share=dividend_rate,
                book_value_per_share=book_value,
                revenue_growth=revenue_growth,
                earnings_growth=earnings_growth,
                dividend_yield=dividend_yield,
                pe_ratio=pe_ratio,
                pb_ratio=pb_ratio,
                peg_ratio=peg_ratio,
                roe=roe,
                roa=roa,
                debt_to_equity=debt_to_equity / 100 if debt_to_equity else None,  # yfinance returns as percentage
                current_ratio=current_ratio,
                quick_ratio=quick_ratio
            )
            
            return stock_data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_multiple_stocks(self, symbols: List[str]) -> List[StockData]:
        """
        Fetch data for multiple stock symbols.
        
        Args:
            symbols: List of stock ticker symbols
            
        Returns:
            List of StockData objects (excludes failed fetches)
        """
        stocks = []
        for symbol in symbols:
            stock = self.get_stock_data(symbol)
            if stock:
                stocks.append(stock)
        return stocks
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get raw stock info dictionary for detailed analysis.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary with all available stock information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Add computed metrics
            info['52week_high'] = info.get('fiftyTwoWeekHigh', 0)
            info['52week_low'] = info.get('fiftyTwoWeekLow', 0)
            info['52week_change'] = info.get('52WeekChange', 0)
            info['beta'] = info.get('beta', 1)
            info['volatility'] = abs(info.get('52WeekChange', 0))
            
            # Free cash flow
            try:
                cf = ticker.cashflow
                if not cf.empty and 'Free Cash Flow' in cf.index:
                    info['free_cash_flow'] = cf.loc['Free Cash Flow'].iloc[0]
                else:
                    info['free_cash_flow'] = info.get('freeCashflow', 0)
            except Exception:
                info['free_cash_flow'] = info.get('freeCashflow', 0)
            
            # Payout ratio
            info['payout_ratio'] = info.get('payoutRatio', 0)
            
            return info
            
        except Exception as e:
            print(f"Error fetching info for {symbol}: {e}")
            return {}


class StockScreener:
    """
    High-level stock screener that combines data fetching with the screening engine.
    
    This class provides a simple interface for screening stocks based on
    fundamental analysis metrics and various investment strategies.
    
    Screening Rules of Thumb:
    - P/E Ratio: 15-20 reasonable, <15 potentially undervalued, >25 potentially overvalued
    - Debt-to-Equity: <1 is safer, capital-intensive industries may have higher
    - Current Ratio: 2:1 is healthy, <1 may indicate liquidity issues
    - ROE: 15%+ is good, indicates efficient use of equity
    - Dividend Payout: <60% is sustainable
    - P/B Ratio: <1 may indicate undervaluation
    - Free Cash Flow: Should be positive and growing
    """
    
    def __init__(self):
        """Initialize the StockScreener"""
        self.data_provider = DataProvider()
        self.analyzer = StockAnalyzer()
        self.engine = ScreeningEngine()
    
    def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on a single stock.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary with all analysis results and metrics
        """
        # Get raw info for additional data points
        info = self.data_provider.get_stock_info(symbol)
        stock_data = self.data_provider.get_stock_data(symbol)
        
        if not stock_data:
            raise ValueError(f"Could not fetch data for {symbol}")
        
        # Get analysis from the engine
        analysis = self.analyzer.analyze(stock_data)
        
        # Combine all data
        result = {
            'symbol': symbol.upper(),
            'current_price': stock_data.price,
            'market_cap': stock_data.market_cap,
            'pe_ratio': analysis['metrics'].get('pe_ratio', 0),
            'pb_ratio': analysis['metrics'].get('pb_ratio', 0),
            'ps_ratio': analysis['metrics'].get('price_to_sales', 0),
            'peg_ratio': analysis['metrics'].get('peg_ratio', 0),
            'roe': analysis['metrics'].get('roe', 0) / 100,  # Convert back to decimal
            'roa': analysis['metrics'].get('roa', 0) / 100,
            'roic': analysis['metrics'].get('roic', 0) / 100,
            'net_margin': analysis['metrics'].get('net_margin', 0) / 100,
            'gross_margin': analysis['metrics'].get('gross_margin', 0) / 100,
            'operating_margin': analysis['metrics'].get('operating_margin', 0) / 100,
            'revenue_growth': stock_data.revenue_growth / 100,
            'earnings_growth': stock_data.earnings_growth / 100,
            'book_value_growth': 0,  # Not available from basic data
            'fcf_growth': 0,  # Not available from basic data
            'current_ratio': analysis['metrics'].get('current_ratio', 0),
            'quick_ratio': analysis['metrics'].get('quick_ratio', 0),
            'debt_to_equity': analysis['metrics'].get('debt_to_equity', 0),
            'debt_to_assets': analysis['metrics'].get('debt_to_assets', 0),
            'interest_coverage': analysis['metrics'].get('interest_coverage', 0),
            'debt_to_ebitda': 0,  # Not available from basic data
            'dividend_yield': stock_data.dividend_yield / 100,
            'payout_ratio': info.get('payout_ratio', 0) or 0,
            'annual_dividend': stock_data.dividend_per_share,
            'years_of_dividends': 0,  # Not available from basic data
            'free_cash_flow': info.get('free_cash_flow', 0) or 0,
            'operating_cash_flow': info.get('operatingCashflow', 0) or 0,
            'cash_conversion_ratio': 0,  # Not available from basic data
            '52week_high': info.get('52week_high', 0),
            '52week_low': info.get('52week_low', 0),
            '52week_change': info.get('52week_change', 0),
            'beta': info.get('beta', 1),
            'volatility': info.get('volatility', 0),
            'sharpe_ratio': 0,  # Requires historical price data
            'debt_rating': 'N/A',
            'quality_score': analysis.get('quality_score', 0) / 10,
            'ev_ebitda': info.get('enterpriseToEbitda', 0) or 0,
            
            # Signals and scores from our analysis
            'signals': analysis.get('signals', []),
            'risk_score': analysis.get('risk_score', 0),
            'fundamental_strength': analysis.get('fundamental_strength', 'N/A'),
            'valuation_score': analysis.get('valuation_score', 0),
            'growth_score': analysis.get('growth_score', 0),
            'momentum_score': analysis.get('momentum_score', 0)
        }
        
        return result
    
    def batch_analyze(self, symbols: List[str], metrics: List[str] = None) -> pd.DataFrame:
        """
        Analyze multiple stocks and return results as a DataFrame.
        
        Args:
            symbols: List of stock ticker symbols
            metrics: Optional list of metrics to include (includes all if None)
            
        Returns:
            DataFrame with analysis results for all stocks
        """
        results = []
        for symbol in symbols:
            try:
                analysis = self.analyze_stock(symbol)
                results.append(analysis)
            except Exception as e:
                print(f"Error analyzing {symbol}: {e}")
        
        if not results:
            return pd.DataFrame()
        
        df = pd.DataFrame(results)
        
        if metrics:
            # Always include symbol
            cols = ['symbol'] + [m for m in metrics if m in df.columns and m != 'symbol']
            df = df[cols]
        
        return df
    
    def screen_stocks(self, symbols: List[str], strategy=None, criteria: Dict = None) -> pd.DataFrame:
        """
        Screen stocks based on a strategy or custom criteria.
        
        Args:
            symbols: List of stock ticker symbols to screen
            strategy: Optional strategy object with screening logic
            criteria: Optional dictionary of screening criteria
            
        Returns:
            DataFrame with stocks that pass the screening criteria
        """
        # Get data for all stocks
        stocks = self.data_provider.get_multiple_stocks(symbols)
        
        if not stocks:
            return pd.DataFrame()
        
        # If using a strategy object
        if strategy:
            # The strategy should have a 'criteria' attribute
            if hasattr(strategy, 'criteria'):
                criteria = strategy.criteria
        
        # Apply criteria filtering
        if criteria:
            filtered_stocks = self._apply_criteria(stocks, criteria)
        else:
            filtered_stocks = stocks
        
        # Convert to DataFrame
        results = []
        for stock in filtered_stocks:
            analysis = self.analyzer.analyze(stock)
            result = {
                'symbol': stock.symbol,
                'current_price': stock.price,
                'pe_ratio': analysis['metrics'].get('pe_ratio', 0),
                'pb_ratio': analysis['metrics'].get('pb_ratio', 0),
                'roe': analysis['metrics'].get('roe', 0) / 100,
                'roa': analysis['metrics'].get('roa', 0) / 100,
                'dividend_yield': stock.dividend_yield / 100,
                'debt_to_equity': analysis['metrics'].get('debt_to_equity', 0),
                'current_ratio': analysis['metrics'].get('current_ratio', 0),
                'revenue_growth': stock.revenue_growth / 100,
                'earnings_growth': stock.earnings_growth / 100,
                'payout_ratio': 0,  # Would need additional data
                'fundamental_strength': analysis.get('fundamental_strength', 'N/A'),
                'quality_score': analysis.get('quality_score', 0),
                'valuation_score': analysis.get('valuation_score', 0)
            }
            results.append(result)
        
        return pd.DataFrame(results)
    
    def _apply_criteria(self, stocks: List[StockData], criteria: Dict) -> List[StockData]:
        """
        Filter stocks based on criteria dictionary.
        
        Criteria format:
        {
            'pe_ratio': {'min': 5, 'max': 20},
            'roe': {'min': 0.15},
            'debt_to_equity': {'max': 1.0}
        }
        """
        filtered = []
        
        for stock in stocks:
            analysis = self.analyzer.analyze(stock)
            metrics = analysis['metrics']
            
            passes = True
            for metric, bounds in criteria.items():
                # Map criteria names to metric names
                metric_map = {
                    'pe_ratio': 'pe_ratio',
                    'pb_ratio': 'pb_ratio',
                    'roe': 'roe',
                    'roa': 'roa',
                    'debt_to_equity': 'debt_to_equity',
                    'current_ratio': 'current_ratio',
                    'dividend_yield': 'dividend_yield',
                    'revenue_growth': 'revenue_growth',
                    'earnings_growth': 'earnings_growth',
                    'payout_ratio': 'payout_ratio',
                    'interest_coverage': 'interest_coverage',
                    'debt_to_assets': 'debt_to_assets',
                    'free_cash_flow': 'free_cash_flow',
                    'years_of_dividends': 'years_of_dividends'
                }
                
                actual_metric = metric_map.get(metric, metric)
                
                # Get the value (check metrics dict first, then stock attributes)
                if actual_metric in metrics:
                    value = metrics[actual_metric]
                elif hasattr(stock, actual_metric):
                    value = getattr(stock, actual_metric)
                else:
                    continue  # Skip unknown metrics
                
                # Check bounds
                if 'min' in bounds and value < bounds['min']:
                    passes = False
                    break
                if 'max' in bounds and value > bounds['max']:
                    passes = False
                    break
            
            if passes:
                filtered.append(stock)
        
        return filtered
    
    def get_rules_of_thumb_evaluation(self, symbol: str) -> Dict[str, Any]:
        """
        Evaluate a stock against all 12 standard rules of thumb.
        """
        analysis = self.analyze_stock(symbol)
        ticker = yf.Ticker(symbol)
        
        evaluations = []
        overall_score = 0
        max_score = 0
        
        # 1. P/E Ratio (15-20 reasonable)
        pe = analysis.get('pe_ratio', float('inf'))
        pe_eval = {
            'metric': 'P/E Ratio',
            'value': f"{pe:.2f}" if pe != float('inf') else 'N/A',
            'rule': '15-20 is reasonable',
            'status': 'GOOD' if 15 <= pe <= 20 else ('UNDERVALUED' if pe < 15 else 'OVERVALUED'),
            'score': 10 if 15 <= pe <= 20 else (8 if 10 <= pe < 15 else (5 if pe < 30 else 0)),
            'tip': 'Compare to peers and the industry average.'
        }
        evaluations.append(pe_eval)
        
        # 2. Debt-to-Equity (<1 safer)
        de = analysis.get('debt_to_equity', 0)
        de_eval = {
            'metric': 'Debt-to-Equity',
            'value': f"{de:.2f}" if de is not None else 'N/A',
            'rule': '<1 is safer',
            'status': 'HEALTHY' if de and de < 1 else 'HIGH',
            'score': 10 if de and de < 1 else (5 if de and de < 2 else 0),
            'tip': "Ensure company's cash flow can service debt."
        }
        evaluations.append(de_eval)
        
        # 3. Current Ratio (2:1 healthy)
        cr = analysis.get('current_ratio', 0)
        cr_eval = {
            'metric': 'Current Ratio',
            'value': f"{cr:.2f}" if cr else 'N/A',
            'rule': '2:1 is healthy',
            'status': 'HEALTHY' if 1.5 <= cr <= 3 else ('LOW' if cr < 1.5 else 'INEFFICIENT'),
            'score': 10 if 1.8 <= cr <= 2.5 else (7 if 1.5 <= cr <= 3 else 0),
            'tip': 'Too high might suggest inefficient asset use.'
        }
        evaluations.append(cr_eval)
        
        # 4. Revenue Growth (Consistent)
        rev_growth = analysis.get('revenue_growth', 0) * 100
        rev_eval = {
            'metric': 'Revenue Growth (YoY)',
            'value': f"{rev_growth:.1f}%",
            'rule': 'Look for consistent growth',
            'status': 'STABLE' if rev_growth > 5 else 'VOLATILE',
            'score': 10 if rev_growth > 10 else (5 if rev_growth > 0 else 0),
            'tip': 'Sudden jumps or declines may suggest market disruption.'
        }
        evaluations.append(rev_eval)
        
        # 5. EPS Growth
        eps_growth = analysis.get('earnings_growth', 0) * 100
        eps_eval = {
            'metric': 'EPS Growth (YoY)',
            'value': f"{eps_growth:.1f}%",
            'rule': 'Steady or rising',
            'status': 'GROWING' if eps_growth > 0 else 'DECLINING',
            'score': 10 if eps_growth > 10 else (5 if eps_growth > 0 else 0),
            'tip': 'EPS should grow in tandem with revenue.'
        }
        evaluations.append(eps_eval)
        
        # 6. ROE (15%+)
        roe = analysis.get('roe', 0) * 100
        roe_eval = {
            'metric': 'ROE',
            'value': f"{roe:.1f}%",
            'rule': '15%+ is good',
            'status': 'EXCELLENT' if roe >= 15 else 'POOR',
            'score': 10 if roe >= 15 else (5 if roe >= 10 else 0),
            'tip': 'Compare ROE to peers in the same industry.'
        }
        evaluations.append(roe_eval)
        
        # 7. Dividend Payout Ratio (<60%)
        payout = analysis.get('payout_ratio', 0) * 100
        payout_eval = {
            'metric': 'Payout Ratio',
            'value': f"{payout:.1f}%" if payout else 'N/A',
            'rule': '<60% is sustainable',
            'status': 'SUSTAINABLE' if payout < 60 else 'HIGH',
            'score': 10 if 0 < payout < 60 else (5 if 60 <= payout < 80 else 0),
            'tip': 'Very high payout limit growth and reinvestment.'
        }
        evaluations.append(payout_eval)
        
        # 8. P/B Ratio (<1)
        pb = analysis.get('pb_ratio', 0)
        pb_eval = {
            'metric': 'P/B Ratio',
            'value': f"{pb:.2f}" if pb else 'N/A',
            'rule': '<1 suggests undervaluation',
            'status': 'UNDERVALUED' if pb and pb < 1 else 'FAIR/OVER',
            'score': 10 if pb and pb < 1 else (7 if pb and pb < 2 else 3),
            'tip': 'Better for asset-heavy industries.'
        }
        evaluations.append(pb_eval)
        
        # 9. Free Cash Flow
        fcf = analysis.get('free_cash_flow', 0)
        fcf_eval = {
            'metric': 'Free Cash Flow',
            'value': f"${fcf/1e9:.2f}B" if fcf else 'N/A',
            'rule': 'Should be positive and growing',
            'status': 'POSITIVE' if fcf and fcf > 0 else 'NEGATIVE',
            'score': 10 if fcf and fcf > 0 else 0,
            'tip': 'FCF is essential for dividends and debt repayment.'
        }
        evaluations.append(fcf_eval)
        
        # 10. Growth vs Value
        is_growth = pe > 25 or eps_growth > 15
        gv_eval = {
            'metric': 'Category',
            'value': 'Growth' if is_growth else 'Value',
            'rule': 'Growth (High P/E) vs Value (Low P/E)',
            'status': 'ANALYZED',
            'score': 10,
            'tip': 'Value offers safety; Growth offers high reward.'
        }
        evaluations.append(gv_eval)
        
        # 11. Diversification (Portfolio Rule)
        div_eval = {
            'metric': 'Diversification Advice',
            'value': 'Review Weight',
            'rule': 'Max 5% per stock',
            'status': 'ADVICE',
            'score': 10,
            'tip': "Don't put more than 5% of your portfolio into a single stock."
        }
        evaluations.append(div_eval)
        
        # 12. Industry Comparison
        sector = ticker.info.get('sector', 'Unknown')
        ind_eval = {
            'metric': 'Industry Context',
            'value': sector,
            'rule': 'Compare within the same industry',
            'status': 'CONTEXT',
            'score': 10,
            'tip': 'Always compare metrics within the same industry.'
        }
        evaluations.append(ind_eval)
        
        # Summary calculations
        overall_score = sum(e['score'] for e in evaluations)
        max_score = len(evaluations) * 10
        percentage = (overall_score / max_score) * 100
        
        return {
            'symbol': symbol,
            'evaluations': evaluations,
            'overall_score': overall_score,
            'max_score': max_score,
            'percentage': percentage,
            'recommendation': 'STRONG_BUY' if percentage >= 80 else (
                'BUY' if percentage >= 60 else (
                    'HOLD' if percentage >= 40 else 'SELL'
                )
            )
        }
