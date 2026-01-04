"""
Comprehensive Stock Screening Backend Module

This module provides fundamental stock screening and analysis capabilities including:
- Fundamental analysis metrics calculation
- Stock performance analysis
- Multi-strategy screening engine
- Custom strategy building framework
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import statistics
from datetime import datetime


class ScreeningStrategy(Enum):
    """Enumeration of predefined screening strategies"""
    VALUE_INVESTING = "value_investing"
    GROWTH_INVESTING = "growth_investing"
    DIVIDEND_INVESTING = "dividend_investing"
    MOMENTUM_INVESTING = "momentum_investing"
    QUALITY_INVESTING = "quality_investing"
    CONTRARIAN = "contrarian"


@dataclass
class StockData:
    """Data class representing fundamental stock information"""
    symbol: str
    price: float
    eps: float  # Earnings Per Share
    revenue: float
    net_income: float
    total_assets: float
    total_liabilities: float
    cash: float
    debt: float
    shares_outstanding: int
    market_cap: float
    dividend_per_share: float
    book_value_per_share: float
    revenue_growth: float  # YoY percentage
    earnings_growth: float  # YoY percentage
    dividend_yield: float  # Percentage
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    debt_to_assets: Optional[float] = None
    interest_coverage: Optional[float] = None


@dataclass
class ScreeningResult:
    """Data class representing screening results"""
    symbol: str
    score: float
    strategy: ScreeningStrategy
    metrics: Dict[str, float]
    signals: List[str]
    timestamp: datetime


class MetricsCalculator:
    """
    Calculates fundamental analysis metrics for stocks.
    
    Metrics include:
    - Valuation ratios (P/E, P/B, PEG)
    - Profitability ratios (ROE, ROA, Net Margin)
    - Efficiency ratios (Asset Turnover, etc.)
    - Liquidity ratios (Current Ratio, Quick Ratio)
    - Solvency ratios (Debt-to-Equity, Interest Coverage)
    - Growth metrics (Revenue Growth, Earnings Growth)
    """
    
    def __init__(self):
        """Initialize the MetricsCalculator"""
        self.calculated_metrics = {}
    
    def calculate_all_metrics(self, stock: StockData) -> Dict[str, float]:
        """
        Calculate all fundamental metrics for a stock.
        
        Args:
            stock: StockData object containing financial information
            
        Returns:
            Dictionary containing all calculated metrics
        """
        metrics = {}
        
        # Valuation Metrics
        metrics['pe_ratio'] = self._calculate_pe_ratio(stock)
        metrics['pb_ratio'] = self._calculate_pb_ratio(stock)
        metrics['peg_ratio'] = self._calculate_peg_ratio(stock)
        metrics['price_to_sales'] = self._calculate_price_to_sales(stock)
        
        # Profitability Metrics
        metrics['roe'] = self._calculate_roe(stock)
        metrics['roa'] = self._calculate_roa(stock)
        metrics['net_margin'] = self._calculate_net_margin(stock)
        metrics['gross_margin'] = self._calculate_gross_margin(stock)
        metrics['operating_margin'] = self._calculate_operating_margin(stock)
        metrics['roic'] = self._calculate_roic(stock)
        
        # Efficiency Metrics
        metrics['asset_turnover'] = self._calculate_asset_turnover(stock)
        metrics['equity_multiplier'] = self._calculate_equity_multiplier(stock)
        
        # Liquidity Metrics
        metrics['current_ratio'] = self._calculate_current_ratio(stock)
        metrics['quick_ratio'] = self._calculate_quick_ratio(stock)
        metrics['cash_ratio'] = self._calculate_cash_ratio(stock)
        
        # Solvency Metrics
        metrics['debt_to_equity'] = self._calculate_debt_to_equity(stock)
        metrics['debt_to_assets'] = self._calculate_debt_to_assets(stock)
        metrics['equity_ratio'] = self._calculate_equity_ratio(stock)
        metrics['interest_coverage'] = self._calculate_interest_coverage(stock)
        
        # Growth Metrics
        metrics['revenue_growth'] = stock.revenue_growth
        metrics['earnings_growth'] = stock.earnings_growth
        metrics['dividend_yield'] = stock.dividend_yield
        
        # Per-Share Metrics
        metrics['eps'] = stock.eps
        metrics['book_value_per_share'] = stock.book_value_per_share
        metrics['dividend_per_share'] = stock.dividend_per_share
        
        self.calculated_metrics = metrics
        return metrics
    
    @staticmethod
    def _calculate_pe_ratio(stock: StockData) -> float:
        """Calculate Price-to-Earnings ratio"""
        if stock.eps <= 0:
            return float('inf')
        return stock.price / stock.eps
    
    @staticmethod
    def _calculate_pb_ratio(stock: StockData) -> float:
        """Calculate Price-to-Book ratio"""
        if stock.book_value_per_share <= 0:
            return float('inf')
        return stock.price / stock.book_value_per_share
    
    @staticmethod
    def _calculate_peg_ratio(stock: StockData) -> float:
        """Calculate PEG ratio (P/E divided by growth rate)"""
        pe_ratio = stock.price / stock.eps if stock.eps > 0 else float('inf')
        if stock.earnings_growth <= 0:
            return float('inf')
        return pe_ratio / stock.earnings_growth
    
    @staticmethod
    def _calculate_price_to_sales(stock: StockData) -> float:
        """Calculate Price-to-Sales ratio"""
        if stock.revenue <= 0:
            return float('inf')
        return stock.market_cap / stock.revenue
    
    @staticmethod
    def _calculate_roe(stock: StockData) -> float:
        """Calculate Return on Equity (%)"""
        equity = stock.total_assets - stock.total_liabilities
        if equity <= 0:
            return 0
        return (stock.net_income / equity) * 100
    
    @staticmethod
    def _calculate_roa(stock: StockData) -> float:
        """Calculate Return on Assets (%)"""
        if stock.total_assets <= 0:
            return 0
        return (stock.net_income / stock.total_assets) * 100
    
    @staticmethod
    def _calculate_net_margin(stock: StockData) -> float:
        """Calculate Net Profit Margin (%)"""
        if stock.revenue <= 0:
            return 0
        return (stock.net_income / stock.revenue) * 100
    
    @staticmethod
    def _calculate_gross_margin(stock: StockData) -> float:
        """Calculate Gross Profit Margin (%) - approximation"""
        if stock.revenue <= 0:
            return 0
        return (stock.net_income / stock.revenue) * 100
    
    @staticmethod
    def _calculate_operating_margin(stock: StockData) -> float:
        """Calculate Operating Margin (%) - approximation"""
        if stock.revenue <= 0:
            return 0
        return (stock.net_income / stock.revenue) * 100
    
    @staticmethod
    def _calculate_roic(stock: StockData) -> float:
        """Calculate Return on Invested Capital (%)"""
        invested_capital = stock.total_assets - (stock.total_assets - stock.total_liabilities - stock.cash)
        if invested_capital <= 0:
            return 0
        return (stock.net_income / invested_capital) * 100
    
    @staticmethod
    def _calculate_asset_turnover(stock: StockData) -> float:
        """Calculate Asset Turnover ratio"""
        if stock.total_assets <= 0:
            return 0
        return stock.revenue / stock.total_assets
    
    @staticmethod
    def _calculate_equity_multiplier(stock: StockData) -> float:
        """Calculate Equity Multiplier"""
        equity = stock.total_assets - stock.total_liabilities
        if equity <= 0:
            return 0
        return stock.total_assets / equity
    
    @staticmethod
    def _calculate_current_ratio(stock: StockData) -> float:
        """Calculate Current Ratio (simplified)"""
        if stock.total_liabilities <= 0:
            return float('inf')
        return stock.cash / stock.total_liabilities
    
    @staticmethod
    def _calculate_quick_ratio(stock: StockData) -> float:
        """Calculate Quick Ratio (simplified)"""
        if stock.total_liabilities <= 0:
            return float('inf')
        return stock.cash / stock.total_liabilities
    
    @staticmethod
    def _calculate_cash_ratio(stock: StockData) -> float:
        """Calculate Cash Ratio"""
        if stock.total_liabilities <= 0:
            return float('inf')
        return stock.cash / stock.total_liabilities
    
    @staticmethod
    def _calculate_debt_to_equity(stock: StockData) -> float:
        """Calculate Debt-to-Equity ratio"""
        equity = stock.total_assets - stock.total_liabilities
        if equity <= 0:
            return float('inf')
        return stock.debt / equity
    
    @staticmethod
    def _calculate_debt_to_assets(stock: StockData) -> float:
        """Calculate Debt-to-Assets ratio"""
        if stock.total_assets <= 0:
            return 0
        return stock.debt / stock.total_assets
    
    @staticmethod
    def _calculate_equity_ratio(stock: StockData) -> float:
        """Calculate Equity Ratio"""
        if stock.total_assets <= 0:
            return 0
        equity = stock.total_assets - stock.total_liabilities
        return (equity / stock.total_assets) * 100
    
    @staticmethod
    def _calculate_interest_coverage(stock: StockData) -> float:
        """Calculate Interest Coverage ratio (simplified)"""
        if stock.debt <= 0:
            return float('inf')
        interest_expense = stock.debt * 0.05  # Assume 5% interest rate
        if interest_expense <= 0:
            return float('inf')
        return stock.net_income / interest_expense


class StockAnalyzer:
    """
    Analyzes stock performance and generates trading signals.
    
    Features:
    - Technical signal generation (overbought/oversold)
    - Fundamental strength assessment
    - Risk analysis
    - Price momentum analysis
    """
    
    def __init__(self):
        """Initialize the StockAnalyzer"""
        self.metrics_calculator = MetricsCalculator()
    
    def analyze(self, stock: StockData) -> Dict[str, any]:
        """
        Perform comprehensive analysis on a stock.
        
        Args:
            stock: StockData object containing financial information
            
        Returns:
            Dictionary with analysis results including signals and scores
        """
        metrics = self.metrics_calculator.calculate_all_metrics(stock)
        
        analysis = {
            'symbol': stock.symbol,
            'metrics': metrics,
            'signals': self._generate_signals(stock, metrics),
            'risk_score': self._calculate_risk_score(stock, metrics),
            'fundamental_strength': self._assess_fundamental_strength(stock, metrics),
            'valuation_score': self._calculate_valuation_score(metrics),
            'quality_score': self._calculate_quality_score(metrics),
            'growth_score': self._calculate_growth_score(stock, metrics),
            'momentum_score': self._calculate_momentum_score(stock)
        }
        
        return analysis
    
    @staticmethod
    def _generate_signals(stock: StockData, metrics: Dict[str, float]) -> List[str]:
        """Generate trading signals based on metrics"""
        signals = []
        
        # Valuation signals
        if metrics['pe_ratio'] < 15:
            signals.append("UNDERVALUED_PE")
        elif metrics['pe_ratio'] > 30:
            signals.append("OVERVALUED_PE")
        
        if metrics['pb_ratio'] < 1:
            signals.append("UNDERVALUED_BOOK")
        elif metrics['pb_ratio'] > 3:
            signals.append("OVERVALUED_BOOK")
        
        # Profitability signals
        if metrics['roe'] > 15:
            signals.append("HIGH_ROE")
        if metrics['roa'] > 10:
            signals.append("HIGH_ROA")
        if metrics['net_margin'] > 20:
            signals.append("HIGH_MARGIN")
        
        # Growth signals
        if stock.revenue_growth > 20:
            signals.append("HIGH_REVENUE_GROWTH")
        if stock.earnings_growth > 20:
            signals.append("HIGH_EARNINGS_GROWTH")
        
        # Dividend signals
        if stock.dividend_yield > 3:
            signals.append("HIGH_DIVIDEND_YIELD")
        elif stock.dividend_yield > 0:
            signals.append("PAYS_DIVIDEND")
        
        # Liquidity signals
        if metrics['current_ratio'] > 2:
            signals.append("STRONG_LIQUIDITY")
        elif metrics['current_ratio'] < 1:
            signals.append("WEAK_LIQUIDITY")
        
        # Debt signals
        if metrics['debt_to_equity'] < 0.5:
            signals.append("LOW_DEBT")
        elif metrics['debt_to_equity'] > 2:
            signals.append("HIGH_DEBT")
        
        return signals
    
    @staticmethod
    def _calculate_risk_score(stock: StockData, metrics: Dict[str, float]) -> float:
        """
        Calculate risk score (0-100, higher = more risky)
        
        Args:
            stock: StockData object
            metrics: Calculated metrics dictionary
            
        Returns:
            Risk score between 0 and 100
        """
        risk_score = 0
        
        # Liquidity risk
        if metrics['current_ratio'] < 1:
            risk_score += 25
        elif metrics['current_ratio'] < 1.5:
            risk_score += 10
        
        # Debt risk
        if metrics['debt_to_equity'] > 2:
            risk_score += 25
        elif metrics['debt_to_equity'] > 1:
            risk_score += 10
        
        # Profitability risk
        if metrics['roe'] < 5:
            risk_score += 20
        elif metrics['roe'] < 10:
            risk_score += 10
        
        # Growth risk
        if stock.revenue_growth < -10:
            risk_score += 15
        elif stock.revenue_growth < 0:
            risk_score += 5
        
        return min(100, max(0, risk_score))
    
    @staticmethod
    def _assess_fundamental_strength(stock: StockData, metrics: Dict[str, float]) -> str:
        """Assess overall fundamental strength"""
        roe = metrics['roe']
        debt_to_equity = metrics['debt_to_equity']
        current_ratio = metrics['current_ratio']
        revenue_growth = stock.revenue_growth
        
        strength_score = 0
        
        if roe > 15:
            strength_score += 25
        elif roe > 10:
            strength_score += 15
        elif roe > 5:
            strength_score += 5
        
        if debt_to_equity < 0.5:
            strength_score += 25
        elif debt_to_equity < 1:
            strength_score += 15
        elif debt_to_equity < 2:
            strength_score += 5
        
        if current_ratio > 1.5:
            strength_score += 25
        elif current_ratio > 1:
            strength_score += 15
        
        if revenue_growth > 10:
            strength_score += 25
        elif revenue_growth > 5:
            strength_score += 15
        elif revenue_growth > 0:
            strength_score += 5
        
        if strength_score >= 80:
            return "VERY_STRONG"
        elif strength_score >= 60:
            return "STRONG"
        elif strength_score >= 40:
            return "MODERATE"
        elif strength_score >= 20:
            return "WEAK"
        else:
            return "VERY_WEAK"
    
    @staticmethod
    def _calculate_valuation_score(metrics: Dict[str, float]) -> float:
        """Calculate valuation score (0-100, higher = better value)"""
        score = 50  # Start at neutral
        
        pe_ratio = metrics['pe_ratio']
        pb_ratio = metrics['pb_ratio']
        ps_ratio = metrics['price_to_sales']
        
        # P/E ratio scoring
        if pe_ratio < 10:
            score += 20
        elif pe_ratio < 15:
            score += 15
        elif pe_ratio < 20:
            score += 10
        elif pe_ratio < 30:
            score += 5
        else:
            score -= 20
        
        # P/B ratio scoring
        if pb_ratio < 1:
            score += 20
        elif pb_ratio < 1.5:
            score += 10
        elif pb_ratio < 2.5:
            score += 5
        else:
            score -= 10
        
        # P/S ratio scoring
        if ps_ratio < 1:
            score += 10
        elif ps_ratio < 2:
            score += 5
        
        return min(100, max(0, score))
    
    @staticmethod
    def _calculate_quality_score(metrics: Dict[str, float]) -> float:
        """Calculate quality score (0-100, higher = better quality)"""
        score = 50  # Start at neutral
        
        # ROE scoring
        if metrics['roe'] > 20:
            score += 20
        elif metrics['roe'] > 15:
            score += 15
        elif metrics['roe'] > 10:
            score += 10
        
        # ROA scoring
        if metrics['roa'] > 10:
            score += 15
        elif metrics['roa'] > 5:
            score += 10
        
        # Net margin scoring
        if metrics['net_margin'] > 20:
            score += 15
        elif metrics['net_margin'] > 10:
            score += 10
        
        # Debt scoring
        if metrics['debt_to_equity'] < 0.5:
            score += 20
        elif metrics['debt_to_equity'] < 1:
            score += 10
        elif metrics['debt_to_equity'] > 2:
            score -= 15
        
        # Current ratio scoring
        if metrics['current_ratio'] > 2:
            score += 10
        elif metrics['current_ratio'] < 1:
            score -= 20
        
        return min(100, max(0, score))
    
    @staticmethod
    def _calculate_growth_score(stock: StockData, metrics: Dict[str, float]) -> float:
        """Calculate growth score (0-100, higher = faster growth)"""
        score = 50  # Start at neutral
        
        # Revenue growth scoring
        if stock.revenue_growth > 30:
            score += 25
        elif stock.revenue_growth > 20:
            score += 20
        elif stock.revenue_growth > 10:
            score += 15
        elif stock.revenue_growth > 5:
            score += 10
        elif stock.revenue_growth < 0:
            score -= 25
        
        # Earnings growth scoring
        if stock.earnings_growth > 30:
            score += 25
        elif stock.earnings_growth > 20:
            score += 20
        elif stock.earnings_growth > 10:
            score += 15
        elif stock.earnings_growth > 5:
            score += 10
        elif stock.earnings_growth < 0:
            score -= 25
        
        # PEG ratio scoring (lower is better for growth)
        peg = metrics['peg_ratio']
        if peg < 1 and stock.earnings_growth > 0:
            score += 20
        elif peg < 2 and stock.earnings_growth > 0:
            score += 10
        
        return min(100, max(0, score))
    
    @staticmethod
    def _calculate_momentum_score(stock: StockData) -> float:
        """Calculate momentum score (0-100)"""
        # In a real implementation, this would use historical price data
        # For now, we use growth metrics as a proxy
        score = 50
        
        if stock.revenue_growth > 15:
            score += 25
        if stock.earnings_growth > 15:
            score += 25
        
        return min(100, max(0, score))


class ScreeningEngine:
    """
    Multi-strategy stock screening engine.
    
    Supports multiple screening strategies:
    - Value Investing
    - Growth Investing
    - Dividend Investing
    - Momentum Investing
    - Quality Investing
    - Contrarian
    """
    
    def __init__(self):
        """Initialize the ScreeningEngine"""
        self.analyzer = StockAnalyzer()
        self.strategies = {
            ScreeningStrategy.VALUE_INVESTING: self._screen_value,
            ScreeningStrategy.GROWTH_INVESTING: self._screen_growth,
            ScreeningStrategy.DIVIDEND_INVESTING: self._screen_dividend,
            ScreeningStrategy.MOMENTUM_INVESTING: self._screen_momentum,
            ScreeningStrategy.QUALITY_INVESTING: self._screen_quality,
            ScreeningStrategy.CONTRARIAN: self._screen_contrarian
        }
    
    def screen(self, stocks: List[StockData], strategy: ScreeningStrategy,
               threshold: float = 50.0) -> List[ScreeningResult]:
        """
        Screen stocks using specified strategy.
        
        Args:
            stocks: List of StockData objects
            strategy: ScreeningStrategy to use
            threshold: Minimum score to include stock (0-100)
            
        Returns:
            List of ScreeningResult objects, sorted by score descending
        """
        results = []
        
        screening_func = self.strategies.get(strategy)
        if not screening_func:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        for stock in stocks:
            analysis = self.analyzer.analyze(stock)
            score, signals = screening_func(stock, analysis)
            
            if score >= threshold:
                result = ScreeningResult(
                    symbol=stock.symbol,
                    score=score,
                    strategy=strategy,
                    metrics=analysis['metrics'],
                    signals=signals,
                    timestamp=datetime.utcnow()
                )
                results.append(result)
        
        return sorted(results, key=lambda x: x.score, reverse=True)
    
    def _screen_value(self, stock: StockData, analysis: Dict) -> Tuple[float, List[str]]:
        """Screen for value investing opportunities"""
        score = 0
        signals = []
        
        pe_ratio = analysis['metrics']['pe_ratio']
        pb_ratio = analysis['metrics']['pb_ratio']
        ps_ratio = analysis['metrics']['price_to_sales']
        roe = analysis['metrics']['roe']
        
        # Low P/E ratio
        if pe_ratio < 10:
            score += 30
            signals.append("VERY_LOW_PE")
        elif pe_ratio < 15:
            score += 20
            signals.append("LOW_PE")
        elif pe_ratio < 20:
            score += 10
        
        # Low P/B ratio
        if pb_ratio < 1:
            score += 25
            signals.append("LOW_PB")
        elif pb_ratio < 1.5:
            score += 15
        
        # Low P/S ratio
        if ps_ratio < 1:
            score += 15
            signals.append("LOW_PS")
        elif ps_ratio < 2:
            score += 10
        
        # Decent ROE
        if roe > 10:
            score += 20
            signals.append("DECENT_ROE")
        
        # Stable earnings
        if stock.earnings_growth >= 0:
            score += 10
        
        return min(100, score), signals
    
    def _screen_growth(self, stock: StockData, analysis: Dict) -> Tuple[float, List[str]]:
        """Screen for growth investing opportunities"""
        score = 0
        signals = []
        
        revenue_growth = stock.revenue_growth
        earnings_growth = stock.earnings_growth
        peg_ratio = analysis['metrics']['peg_ratio']
        roe = analysis['metrics']['roe']
        
        # High revenue growth
        if revenue_growth > 30:
            score += 30
            signals.append("VERY_HIGH_REVENUE_GROWTH")
        elif revenue_growth > 20:
            score += 25
            signals.append("HIGH_REVENUE_GROWTH")
        elif revenue_growth > 10:
            score += 15
        
        # High earnings growth
        if earnings_growth > 30:
            score += 30
            signals.append("VERY_HIGH_EARNINGS_GROWTH")
        elif earnings_growth > 20:
            score += 25
            signals.append("HIGH_EARNINGS_GROWTH")
        elif earnings_growth > 10:
            score += 15
        
        # Good PEG ratio
        if peg_ratio < 1:
            score += 20
            signals.append("GOOD_PEG")
        elif peg_ratio < 2:
            score += 10
        
        # Decent ROE
        if roe > 15:
            score += 15
        
        return min(100, score), signals
    
    def _screen_dividend(self, stock: StockData, analysis: Dict) -> Tuple[float, List[str]]:
        """Screen for dividend investing opportunities"""
        score = 0
        signals = []
        
        dividend_yield = stock.dividend_yield
        dps = stock.dividend_per_share
        roe = analysis['metrics']['roe']
        debt_to_equity = analysis['metrics']['debt_to_equity']
        
        # Dividend yield
        if dividend_yield >= 5:
            score += 30
            signals.append("VERY_HIGH_YIELD")
        elif dividend_yield >= 3:
            score += 25
            signals.append("HIGH_YIELD")
        elif dividend_yield >= 2:
            score += 15
            signals.append("MODERATE_YIELD")
        elif dps > 0:
            score += 5
            signals.append("PAYS_DIVIDEND")
        
        # Sustainable dividends (decent ROE)
        if roe > 10:
            score += 20
            signals.append("SUSTAINABLE_DIVIDEND")
        
        # Low debt
        if debt_to_equity < 1:
            score += 15
        elif debt_to_equity < 2:
            score += 10
        
        # Stable earnings
        if stock.earnings_growth >= -5:
            score += 10
        
        return min(100, score), signals
    
    def _screen_momentum(self, stock: StockData, analysis: Dict) -> Tuple[float, List[str]]:
        """Screen for momentum investing opportunities"""
        score = 0
        signals = []
        
        revenue_growth = stock.revenue_growth
        earnings_growth = stock.earnings_growth
        momentum_score = analysis['momentum_score']
        
        # High growth rates indicate momentum
        if earnings_growth > 25:
            score += 35
            signals.append("STRONG_MOMENTUM")
        elif earnings_growth > 15:
            score += 25
            signals.append("MODERATE_MOMENTUM")
        elif earnings_growth > 5:
            score += 15
        
        # Revenue growth supports momentum
        if revenue_growth > 20:
            score += 20
        
        # Use analyzer's momentum score
        if momentum_score > 70:
            score += 15
        
        return min(100, score), signals
    
    def _screen_quality(self, stock: StockData, analysis: Dict) -> Tuple[float, List[str]]:
        """Screen for quality investing opportunities"""
        score = 0
        signals = []
        
        quality_score = analysis['quality_score']
        roe = analysis['metrics']['roe']
        roa = analysis['metrics']['roa']
        debt_to_equity = analysis['metrics']['debt_to_equity']
        current_ratio = analysis['metrics']['current_ratio']
        net_margin = analysis['metrics']['net_margin']
        
        # High quality score
        if quality_score > 80:
            score += 30
            signals.append("HIGH_QUALITY")
        elif quality_score > 70:
            score += 20
            signals.append("GOOD_QUALITY")
        
        # Strong profitability
        if roe > 20:
            score += 20
            signals.append("EXCELLENT_ROE")
        elif roe > 15:
            score += 15
        
        if roa > 10:
            score += 15
        
        # Low debt
        if debt_to_equity < 0.5:
            score += 20
            signals.append("VERY_LOW_DEBT")
        elif debt_to_equity < 1:
            score += 10
        
        # Strong liquidity
        if current_ratio > 2:
            score += 10
            signals.append("STRONG_LIQUIDITY")
        
        # Good margins
        if net_margin > 15:
            score += 10
        
        return min(100, score), signals
    
    def _screen_contrarian(self, stock: StockData, analysis: Dict) -> Tuple[float, List[str]]:
        """Screen for contrarian investing opportunities"""
        score = 0
        signals = []
        
        pe_ratio = analysis['metrics']['pe_ratio']
        pb_ratio = analysis['metrics']['pb_ratio']
        valuation_score = analysis['valuation_score']
        revenue_growth = stock.revenue_growth
        roe = analysis['metrics']['roe']
        
        # Very low valuation (market pessimism)
        if pe_ratio < 8:
            score += 30
            signals.append("EXTREMELY_UNDERVALUED")
        elif pe_ratio < 12:
            score += 20
            signals.append("SIGNIFICANTLY_UNDERVALUED")
        
        if pb_ratio < 0.8:
            score += 20
        
        # Low valuation score means market undervalues it
        if valuation_score > 70:
            score += 25
            signals.append("MARKET_UNDERVALUATION")
        
        # But with hidden quality
        if roe > 10 and revenue_growth >= 0:
            score += 20
            signals.append("HIDDEN_VALUE")
        
        return min(100, score), signals


class StrategyBuilder:
    """
    Custom screening strategy builder.
    
    Allows users to define custom screening strategies using a flexible
    rule-based system. Users can combine multiple conditions with AND/OR logic.
    """
    
    def __init__(self):
        """Initialize the StrategyBuilder"""
        self.analyzer = StockAnalyzer()
        self.custom_strategies = {}
    
    def create_strategy(self, name: str, rules: List[Callable]) -> str:
        """
        Create a custom screening strategy.
        
        Args:
            name: Name for the custom strategy
            rules: List of rule functions that take StockData and return bool
            
        Returns:
            Strategy ID
        """
        strategy_id = f"custom_{name}_{len(self.custom_strategies)}"
        self.custom_strategies[strategy_id] = {
            'name': name,
            'rules': rules,
            'created_at': datetime.utcnow()
        }
        return strategy_id
    
    def screen_with_custom_strategy(self, stocks: List[StockData],
                                   strategy_id: str,
                                   threshold: float = 50.0) -> List[ScreeningResult]:
        """
        Screen stocks using a custom strategy.
        
        Args:
            stocks: List of StockData objects
            strategy_id: ID of custom strategy
            threshold: Minimum score to include stock
            
        Returns:
            List of ScreeningResult objects
        """
        if strategy_id not in self.custom_strategies:
            raise ValueError(f"Unknown strategy ID: {strategy_id}")
        
        strategy = self.custom_strategies[strategy_id]
        results = []
        
        for stock in stocks:
            analysis = self.analyzer.analyze(stock)
            
            # Apply all rules
            match_count = 0
            matching_signals = []
            
            for i, rule in enumerate(strategy['rules']):
                try:
                    if rule(stock, analysis):
                        match_count += 1
                        matching_signals.append(f"RULE_{i}")
                except Exception as e:
                    print(f"Error evaluating rule {i}: {e}")
            
            # Score based on how many rules matched
            score = (match_count / len(strategy['rules'])) * 100
            
            if score >= threshold:
                result = ScreeningResult(
                    symbol=stock.symbol,
                    score=score,
                    strategy=ScreeningStrategy.VALUE_INVESTING,  # Generic strategy
                    metrics=analysis['metrics'],
                    signals=matching_signals,
                    timestamp=datetime.utcnow()
                )
                results.append(result)
        
        return sorted(results, key=lambda x: x.score, reverse=True)
    
    def create_pe_based_strategy(self, pe_min: float = 10, pe_max: float = 20) -> str:
        """
        Create a P/E ratio-based screening strategy.
        
        Args:
            pe_min: Minimum P/E ratio
            pe_max: Maximum P/E ratio
            
        Returns:
            Strategy ID
        """
        def pe_rule(stock: StockData, analysis: Dict) -> bool:
            pe = analysis['metrics']['pe_ratio']
            return pe_min <= pe <= pe_max
        
        return self.create_strategy(f"pe_{pe_min}_{pe_max}", [pe_rule])
    
    def create_quality_screen_strategy(self, min_roe: float = 15,
                                      max_debt_to_equity: float = 1.0) -> str:
        """
        Create a quality screen strategy.
        
        Args:
            min_roe: Minimum ROE (%)
            max_debt_to_equity: Maximum Debt-to-Equity ratio
            
        Returns:
            Strategy ID
        """
        def roe_rule(stock: StockData, analysis: Dict) -> bool:
            return analysis['metrics']['roe'] >= min_roe
        
        def debt_rule(stock: StockData, analysis: Dict) -> bool:
            return analysis['metrics']['debt_to_equity'] <= max_debt_to_equity
        
        def liquidity_rule(stock: StockData, analysis: Dict) -> bool:
            return analysis['metrics']['current_ratio'] >= 1.5
        
        return self.create_strategy("quality_screen", [roe_rule, debt_rule, liquidity_rule])
    
    def create_growth_screen_strategy(self, min_revenue_growth: float = 15,
                                     min_earnings_growth: float = 15) -> str:
        """
        Create a growth screen strategy.
        
        Args:
            min_revenue_growth: Minimum revenue growth (%)
            min_earnings_growth: Minimum earnings growth (%)
            
        Returns:
            Strategy ID
        """
        def revenue_rule(stock: StockData, analysis: Dict) -> bool:
            return stock.revenue_growth >= min_revenue_growth
        
        def earnings_rule(stock: StockData, analysis: Dict) -> bool:
            return stock.earnings_growth >= min_earnings_growth
        
        def peg_rule(stock: StockData, analysis: Dict) -> bool:
            peg = analysis['metrics']['peg_ratio']
            return peg < 2 and peg != float('inf')
        
        return self.create_strategy("growth_screen", [revenue_rule, earnings_rule, peg_rule])
    
    def create_dividend_screen_strategy(self, min_yield: float = 3.0) -> str:
        """
        Create a dividend screen strategy.
        
        Args:
            min_yield: Minimum dividend yield (%)
            
        Returns:
            Strategy ID
        """
        def yield_rule(stock: StockData, analysis: Dict) -> bool:
            return stock.dividend_yield >= min_yield
        
        def sustainability_rule(stock: StockData, analysis: Dict) -> bool:
            return analysis['metrics']['roe'] >= 10 and analysis['metrics']['debt_to_equity'] < 1
        
        return self.create_strategy("dividend_screen", [yield_rule, sustainability_rule])
    
    def get_strategy_info(self, strategy_id: str) -> Dict:
        """Get information about a custom strategy"""
        if strategy_id not in self.custom_strategies:
            raise ValueError(f"Unknown strategy ID: {strategy_id}")
        return self.custom_strategies[strategy_id]
    
    def list_strategies(self) -> List[str]:
        """List all custom strategy IDs"""
        return list(self.custom_strategies.keys())


# Helper function for batch screening
def batch_screen(stocks: List[StockData],
                strategies: List[ScreeningStrategy],
                threshold: float = 50.0) -> Dict[str, List[ScreeningResult]]:
    """
    Screen stocks using multiple strategies simultaneously.
    
    Args:
        stocks: List of StockData objects
        strategies: List of ScreeningStrategy enums
        threshold: Minimum score to include stock
        
    Returns:
        Dictionary mapping strategy names to lists of ScreeningResult objects
    """
    engine = ScreeningEngine()
    results = {}
    
    for strategy in strategies:
        results[strategy.value] = engine.screen(stocks, strategy, threshold)
    
    return results
