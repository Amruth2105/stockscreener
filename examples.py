"""
Comprehensive usage examples for the stock screener module.

This module demonstrates all features of the stock screener including:
- Basic stock analysis
- Value investing strategies
- Growth investing strategies
- Dividend investing strategies
- Quality investing strategies
- Batch screening
- Custom screening strategies
- Comprehensive metrics reporting
"""

from stock_screener import StockScreener, ScreeningStrategy
from stock_screener.strategies import (
    ValueStrategy,
    GrowthStrategy,
    DividendStrategy,
    QualityStrategy
)
import pandas as pd
from datetime import datetime


# ============================================================================
# EXAMPLE 1: BASIC STOCK ANALYSIS
# ============================================================================

def example_basic_analysis():
    """
    Demonstrates basic stock analysis functionality.
    Shows how to fetch and analyze a single stock.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: BASIC STOCK ANALYSIS")
    print("="*70)
    
    # Initialize the screener
    screener = StockScreener()
    
    # Analyze a single stock
    symbol = "AAPL"
    print(f"\nAnalyzing {symbol}...")
    
    analysis = screener.analyze_stock(symbol)
    
    # Display basic metrics
    print(f"\nBasic Metrics for {symbol}:")
    print(f"  Current Price: ${analysis['current_price']:.2f}")
    print(f"  Market Cap: ${analysis['market_cap']:.2e}")
    print(f"  P/E Ratio: {analysis['pe_ratio']:.2f}")
    print(f"  P/B Ratio: {analysis['pb_ratio']:.2f}")
    print(f"  Debt-to-Equity: {analysis['debt_to_equity']:.2f}")
    print(f"  ROE: {analysis['roe']:.2%}")
    print(f"  ROA: {analysis['roa']:.2%}")
    print(f"  Current Ratio: {analysis['current_ratio']:.2f}")
    print(f"  52-Week High: ${analysis['52week_high']:.2f}")
    print(f"  52-Week Low: ${analysis['52week_low']:.2f}")
    
    return analysis


# ============================================================================
# EXAMPLE 2: VALUE INVESTING STRATEGY
# ============================================================================

def example_value_investing():
    """
    Demonstrates value investing strategy.
    Identifies undervalued stocks based on fundamental metrics.
    
    Value investing criteria:
    - Low P/E ratio
    - Low P/B ratio
    - High dividend yield
    - Strong book value
    - Reasonable debt levels
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: VALUE INVESTING STRATEGY")
    print("="*70)
    
    screener = StockScreener()
    
    # Define value investing criteria
    value_criteria = {
        'pe_ratio': {'max': 15},              # P/E less than 15
        'pb_ratio': {'max': 1.5},             # P/B less than 1.5
        'dividend_yield': {'min': 0.02},      # At least 2% dividend yield
        'debt_to_equity': {'max': 1.0},       # D/E ratio less than 1
        'current_ratio': {'min': 1.5},        # Current ratio above 1.5
        'roe': {'min': 0.10}                  # ROE above 10%
    }
    
    # Common large-cap stocks to screen
    stocks = ['KO', 'MCD', 'JNJ', 'PG', 'WMT', 'PEP', 'MSFT']
    
    print(f"\nScreening {len(stocks)} stocks for value investing opportunities...")
    print(f"Criteria: {value_criteria}\n")
    
    value_strategy = ValueStrategy(criteria=value_criteria)
    results = screener.screen_stocks(stocks, strategy=value_strategy)
    
    # Display results
    if results.empty:
        print("No stocks met the value investing criteria.")
    else:
        print(f"Found {len(results)} value stocks:\n")
        print(results[['symbol', 'current_price', 'pe_ratio', 'pb_ratio', 
                      'dividend_yield', 'roe']].to_string())
    
    return results


# ============================================================================
# EXAMPLE 3: GROWTH INVESTING STRATEGY
# ============================================================================

def example_growth_investing():
    """
    Demonstrates growth investing strategy.
    Identifies stocks with strong growth potential.
    
    Growth investing criteria:
    - Revenue growth > 15%
    - Earnings growth > 15%
    - Low dividend yield (reinvesting profits)
    - High ROE
    - P/E to growth ratio < 2
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: GROWTH INVESTING STRATEGY")
    print("="*70)
    
    screener = StockScreener()
    
    # Define growth investing criteria
    growth_criteria = {
        'revenue_growth': {'min': 0.15},      # At least 15% revenue growth
        'earnings_growth': {'min': 0.15},     # At least 15% earnings growth
        'dividend_yield': {'max': 0.02},      # Less than 2% dividend yield
        'roe': {'min': 0.15},                 # ROE above 15%
        'pe_ratio': {'min': 15, 'max': 50},   # P/E between 15 and 50
    }
    
    # Technology and growth stocks
    stocks = ['TSLA', 'NVDA', 'AMD', 'SNOW', 'ROKU', 'SQ', 'NET']
    
    print(f"\nScreening {len(stocks)} stocks for growth investing opportunities...")
    print(f"Criteria: {growth_criteria}\n")
    
    growth_strategy = GrowthStrategy(criteria=growth_criteria)
    results = screener.screen_stocks(stocks, strategy=growth_strategy)
    
    # Display results
    if results.empty:
        print("No stocks met the growth investing criteria.")
    else:
        print(f"Found {len(results)} growth stocks:\n")
        print(results[['symbol', 'current_price', 'revenue_growth', 
                      'earnings_growth', 'roe', 'pe_ratio']].to_string())
    
    return results


# ============================================================================
# EXAMPLE 4: DIVIDEND INVESTING STRATEGY
# ============================================================================

def example_dividend_investing():
    """
    Demonstrates dividend investing strategy.
    Identifies stocks with attractive dividend yields and payment history.
    
    Dividend investing criteria:
    - Dividend yield > 3%
    - Stable dividend payment history
    - Payout ratio < 70%
    - Strong cash flow
    - Sustainable dividend
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: DIVIDEND INVESTING STRATEGY")
    print("="*70)
    
    screener = StockScreener()
    
    # Define dividend investing criteria
    dividend_criteria = {
        'dividend_yield': {'min': 0.03},      # At least 3% dividend yield
        'payout_ratio': {'max': 0.70},        # Payout ratio less than 70%
        'free_cash_flow': {'min': 1e9},       # At least $1B free cash flow
        'years_of_dividends': {'min': 10},    # At least 10 years of payments
        'current_ratio': {'min': 1.0},        # Current ratio above 1.0
    }
    
    # Dividend aristocrats and high-yield stocks
    stocks = ['JNJ', 'PG', 'KO', 'MO', 'T', 'VZ', 'O', 'SCHD']
    
    print(f"\nScreening {len(stocks)} stocks for dividend investing opportunities...")
    print(f"Criteria: {dividend_criteria}\n")
    
    dividend_strategy = DividendStrategy(criteria=dividend_criteria)
    results = screener.screen_stocks(stocks, strategy=dividend_strategy)
    
    # Display results
    if results.empty:
        print("No stocks met the dividend investing criteria.")
    else:
        print(f"Found {len(results)} dividend stocks:\n")
        print(results[['symbol', 'current_price', 'dividend_yield', 
                      'payout_ratio', 'years_of_dividends']].to_string())
    
    return results


# ============================================================================
# EXAMPLE 5: QUALITY INVESTING STRATEGY
# ============================================================================

def example_quality_investing():
    """
    Demonstrates quality investing strategy.
    Identifies high-quality companies with strong fundamentals.
    
    Quality investing criteria:
    - High ROE (>15%)
    - Low debt-to-equity (<1.0)
    - Strong current ratio (>2.0)
    - Consistent earnings
    - Low volatility
    - Strong competitive moat
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: QUALITY INVESTING STRATEGY")
    print("="*70)
    
    screener = StockScreener()
    
    # Define quality investing criteria
    quality_criteria = {
        'roe': {'min': 0.15},                 # ROE above 15%
        'roa': {'min': 0.10},                 # ROA above 10%
        'debt_to_equity': {'max': 1.0},       # D/E ratio less than 1
        'current_ratio': {'min': 2.0},        # Current ratio above 2.0
        'interest_coverage': {'min': 5.0},    # Interest coverage > 5x
        'debt_to_assets': {'max': 0.5},       # Debt to assets < 50%
    }
    
    # Quality large-cap stocks
    stocks = ['MSFT', 'AAPL', 'V', 'JNJ', 'WMT', 'UNH', 'MA']
    
    print(f"\nScreening {len(stocks)} stocks for quality investing opportunities...")
    print(f"Criteria: {quality_criteria}\n")
    
    quality_strategy = QualityStrategy(criteria=quality_criteria)
    results = screener.screen_stocks(stocks, strategy=quality_strategy)
    
    # Display results
    if results.empty:
        print("No stocks met the quality investing criteria.")
    else:
        print(f"Found {len(results)} quality stocks:\n")
        print(results[['symbol', 'current_price', 'roe', 'roa', 
                      'debt_to_equity', 'current_ratio']].to_string())
    
    return results


# ============================================================================
# EXAMPLE 6: BATCH SCREENING
# ============================================================================

def example_batch_screening():
    """
    Demonstrates batch screening of multiple stocks at once.
    Shows how to screen a large portfolio efficiently.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: BATCH SCREENING")
    print("="*70)
    
    screener = StockScreener()
    
    # Large portfolio of stocks
    stocks = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK.B',
        'JNJ', 'V', 'WMT', 'PG', 'MA', 'HD', 'KO', 'MCD', 'NKE', 'ADBE',
        'CRM', 'CSCO', 'IBM', 'INTC', 'AMD', 'NFLX', 'AVGO', 'QCOM'
    ]
    
    print(f"\nBatch screening {len(stocks)} stocks...")
    
    # Screen all stocks with multiple criteria
    results = screener.batch_analyze(stocks, metrics=[
        'current_price', 'pe_ratio', 'pb_ratio', 'dividend_yield',
        'roe', 'roa', 'debt_to_equity', 'current_ratio'
    ])
    
    print(f"\nScanned {len(results)} stocks successfully.")
    print(f"\nTop 10 stocks by P/E ratio (lowest first):")
    top_pe = results.nsmallest(10, 'pe_ratio')[['symbol', 'current_price', 'pe_ratio']]
    print(top_pe.to_string())
    
    print(f"\nTop 10 stocks by dividend yield (highest first):")
    top_div = results.nlargest(10, 'dividend_yield')[['symbol', 'dividend_yield']]
    print(top_div.to_string())
    
    print(f"\nTop 10 stocks by ROE (highest first):")
    top_roe = results.nlargest(10, 'roe')[['symbol', 'roe']]
    print(top_roe.to_string())
    
    return results


# ============================================================================
# EXAMPLE 7: CUSTOM SCREENING STRATEGY
# ============================================================================

def example_custom_strategy():
    """
    Demonstrates creation and use of custom screening strategies.
    Shows how to define custom criteria for specific investment goals.
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: CUSTOM SCREENING STRATEGY")
    print("="*70)
    
    screener = StockScreener()
    
    # Define a custom strategy combining multiple criteria
    # Strategy: "Dividend Growth" - High yield with growing earnings
    custom_criteria = {
        'dividend_yield': {'min': 0.025, 'max': 0.08},  # 2.5-8% yield
        'earnings_growth': {'min': 0.05},                # At least 5% growth
        'payout_ratio': {'max': 0.60},                   # Below 60% payout
        'debt_to_equity': {'max': 1.5},                  # Reasonable debt
        'free_cash_flow': {'min': 5e8},                  # At least $500M FCF
        'pe_ratio': {'min': 10, 'max': 25},              # P/E between 10-25
    }
    
    stocks = ['JNJ', 'PG', 'KO', 'MCD', 'PEP', 'VZ', 'T', 'O', 'SCHD']
    
    print("\nCustom Strategy: Dividend Growth Stocks")
    print(f"Criteria: {custom_criteria}\n")
    
    custom_strategy = ScreeningStrategy(
        name="Dividend Growth",
        criteria=custom_criteria,
        description="High dividend yield with growing earnings"
    )
    
    results = screener.screen_stocks(stocks, strategy=custom_strategy)
    
    if results.empty:
        print("No stocks met the custom criteria.")
    else:
        print(f"Found {len(results)} dividend growth stocks:\n")
        print(results[['symbol', 'current_price', 'dividend_yield', 
                      'earnings_growth', 'payout_ratio']].to_string())
    
    return results


# ============================================================================
# EXAMPLE 8: COMPREHENSIVE METRICS REPORTING
# ============================================================================

def example_comprehensive_reporting():
    """
    Demonstrates comprehensive metrics reporting and analysis.
    Shows how to generate detailed reports with all available metrics.
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: COMPREHENSIVE METRICS REPORTING")
    print("="*70)
    
    screener = StockScreener()
    
    # Select stocks for detailed analysis
    stocks = ['AAPL', 'MSFT', 'JNJ', 'V', 'MA']
    
    print(f"\nGenerating comprehensive report for {len(stocks)} stocks...\n")
    
    for symbol in stocks:
        print(f"\n{'-'*70}")
        print(f"DETAILED ANALYSIS: {symbol}")
        print(f"{'-'*70}")
        
        analysis = screener.analyze_stock(symbol)
        
        # Valuation Metrics
        print("\n📊 VALUATION METRICS:")
        print(f"  Current Price: ${analysis['current_price']:.2f}")
        print(f"  Market Cap: ${analysis['market_cap']:,.0f}")
        print(f"  P/E Ratio: {analysis['pe_ratio']:.2f}")
        print(f"  P/B Ratio: {analysis['pb_ratio']:.2f}")
        print(f"  P/S Ratio: {analysis['ps_ratio']:.2f}")
        print(f"  EV/EBITDA: {analysis['ev_ebitda']:.2f}")
        
        # Profitability Metrics
        print("\n💰 PROFITABILITY METRICS:")
        print(f"  ROE (Return on Equity): {analysis['roe']:.2%}")
        print(f"  ROA (Return on Assets): {analysis['roa']:.2%}")
        print(f"  ROIC (Return on Invested Capital): {analysis['roic']:.2%}")
        print(f"  Net Profit Margin: {analysis['net_margin']:.2%}")
        print(f"  Gross Profit Margin: {analysis['gross_margin']:.2%}")
        print(f"  Operating Margin: {analysis['operating_margin']:.2%}")
        
        # Growth Metrics
        print("\n📈 GROWTH METRICS:")
        print(f"  Revenue Growth (YoY): {analysis['revenue_growth']:.2%}")
        print(f"  Earnings Growth (YoY): {analysis['earnings_growth']:.2%}")
        print(f"  Book Value Growth: {analysis['book_value_growth']:.2%}")
        print(f"  Free Cash Flow Growth: {analysis['fcf_growth']:.2%}")
        
        # Financial Health Metrics
        print("\n🏥 FINANCIAL HEALTH METRICS:")
        print(f"  Current Ratio: {analysis['current_ratio']:.2f}")
        print(f"  Quick Ratio: {analysis['quick_ratio']:.2f}")
        print(f"  Debt-to-Equity: {analysis['debt_to_equity']:.2f}")
        print(f"  Debt-to-Assets: {analysis['debt_to_assets']:.2f}")
        print(f"  Interest Coverage: {analysis['interest_coverage']:.2f}x")
        print(f"  Debt to EBITDA: {analysis['debt_to_ebitda']:.2f}x")
        
        # Dividend Metrics
        print("\n💵 DIVIDEND METRICS:")
        print(f"  Dividend Yield: {analysis['dividend_yield']:.2%}")
        print(f"  Dividend Payout Ratio: {analysis['payout_ratio']:.2%}")
        print(f"  Annual Dividend: ${analysis['annual_dividend']:.2f}")
        print(f"  Years of Dividend Growth: {analysis['years_of_dividends']}")
        
        # Cash Flow Metrics
        print("\n💧 CASH FLOW METRICS:")
        print(f"  Free Cash Flow: ${analysis['free_cash_flow']:,.0f}")
        print(f"  Operating Cash Flow: ${analysis['operating_cash_flow']:,.0f}")
        print(f"  Cash Conversion Ratio: {analysis['cash_conversion_ratio']:.2%}")
        
        # Price Performance Metrics
        print("\n📊 PRICE PERFORMANCE METRICS:")
        print(f"  52-Week High: ${analysis['52week_high']:.2f}")
        print(f"  52-Week Low: ${analysis['52week_low']:.2f}")
        print(f"  52-Week Change: {analysis['52week_change']:.2%}")
        print(f"  Beta: {analysis['beta']:.2f}")
        print(f"  Volatility (Annual): {analysis['volatility']:.2%}")
        
        # Risk Metrics
        print("\n⚠️  RISK METRICS:")
        print(f"  PEG Ratio: {analysis['peg_ratio']:.2f}")
        print(f"  Sharpe Ratio: {analysis['sharpe_ratio']:.2f}")
        print(f"  Debt Rating: {analysis['debt_rating']}")
        
        # Quality Score
        print("\n⭐ QUALITY SCORE: {:.1f}/10".format(analysis['quality_score']))


# ============================================================================
# EXAMPLE 9: COMPARATIVE ANALYSIS
# ============================================================================

def example_comparative_analysis():
    """
    Demonstrates comparative analysis between multiple stocks.
    Useful for comparing companies within the same sector.
    """
    print("\n" + "="*70)
    print("EXAMPLE 9: COMPARATIVE ANALYSIS")
    print("="*70)
    
    screener = StockScreener()
    
    # Compare tech giants
    tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
    
    print(f"\nComparing {len(tech_stocks)} major technology companies...\n")
    
    results = screener.batch_analyze(tech_stocks, metrics=[
        'current_price', 'market_cap', 'pe_ratio', 'pb_ratio', 'roe', 'roa'
    ])
    
    # Display comparison table
    print("Side-by-side Comparison:")
    print(results[['symbol', 'current_price', 'market_cap', 
                   'pe_ratio', 'pb_ratio', 'roe', 'roa']].to_string())
    
    # Key insights
    print("\n📊 KEY INSIGHTS:")
    print(f"  Lowest P/E Ratio: {results.loc[results['pe_ratio'].idxmin(), 'symbol']} ({results['pe_ratio'].min():.2f})")
    print(f"  Highest P/E Ratio: {results.loc[results['pe_ratio'].idxmax(), 'symbol']} ({results['pe_ratio'].max():.2f})")
    print(f"  Highest ROE: {results.loc[results['roe'].idxmax(), 'symbol']} ({results['roe'].max():.2%})")
    print(f"  Highest ROA: {results.loc[results['roa'].idxmax(), 'symbol']} ({results['roa'].max():.2%})")
    print(f"  Largest by Market Cap: {results.loc[results['market_cap'].idxmax(), 'symbol']} (${results['market_cap'].max():,.0f})")
    
    return results


# ============================================================================
# EXAMPLE 10: PORTFOLIO OPTIMIZATION
# ============================================================================

def example_portfolio_analysis():
    """
    Demonstrates portfolio-level analysis and optimization suggestions.
    Shows how to analyze and balance a portfolio using screening results.
    """
    print("\n" + "="*70)
    print("EXAMPLE 10: PORTFOLIO ANALYSIS & OPTIMIZATION")
    print("="*70)
    
    screener = StockScreener()
    
    # Example portfolio
    portfolio = {
        'AAPL': 10000,
        'MSFT': 8000,
        'JNJ': 5000,
        'V': 6000,
        'KO': 4000,
    }
    
    total_investment = sum(portfolio.values())
    
    print(f"\nAnalyzing portfolio of {len(portfolio)} stocks...")
    print(f"Total Investment: ${total_investment:,.2f}\n")
    
    stocks = list(portfolio.keys())
    results = screener.batch_analyze(stocks)
    
    print("Portfolio Holdings:")
    print(f"{'Symbol':<10} {'Amount':<15} {'Weight':<10} {'P/E':<8} {'Div Yield':<12} {'ROE':<8}")
    print("-" * 65)
    
    for symbol, amount in portfolio.items():
        weight = amount / total_investment
        stock_data = results[results['symbol'] == symbol].iloc[0]
        print(f"{symbol:<10} ${amount:>13,.2f} {weight:>8.1%} {stock_data['pe_ratio']:>7.2f} {stock_data['dividend_yield']:>10.2%} {stock_data['roe']:>7.1%}")
    
    # Portfolio metrics
    print(f"\n{'PORTFOLIO METRICS:':<20}")
    print(f"  Average P/E Ratio: {results['pe_ratio'].mean():.2f}")
    print(f"  Average Dividend Yield: {results['dividend_yield'].mean():.2%}")
    print(f"  Average ROE: {results['roe'].mean():.2%}")
    print(f"  Average Debt-to-Equity: {results['debt_to_equity'].mean():.2f}")
    
    # Recommendations
    print(f"\n💡 PORTFOLIO RECOMMENDATIONS:")
    
    # Diversification check
    avg_pe = results['pe_ratio'].mean()
    overvalued = results[results['pe_ratio'] > avg_pe * 1.2]
    undervalued = results[results['pe_ratio'] < avg_pe * 0.8]
    
    if not overvalued.empty:
        print(f"  • Consider trimming overvalued positions: {', '.join(overvalued['symbol'].tolist())}")
    
    if not undervalued.empty:
        print(f"  • Consider adding to undervalued positions: {', '.join(undervalued['symbol'].tolist())}")
    
    # High dividend stocks check
    high_div = results[results['dividend_yield'] > 0.03]
    if not high_div.empty:
        print(f"  • High dividend income stocks: {', '.join(high_div['symbol'].tolist())}")
    
    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_all_examples():
    """
    Runs all examples in sequence.
    """
    print("\n" + "="*70)
    print("STOCK SCREENER - COMPREHENSIVE USAGE EXAMPLES")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    try:
        # Run selected examples for verification
        import time
        print("Running Example 1...")
        example_basic_analysis()
        time.sleep(2)
        print("Running Example 2...")
        example_value_investing()
        time.sleep(2)
        print("Running Example 3...")
        example_growth_investing()
        # example_dividend_investing()
        # example_quality_investing()
        # example_batch_screening()
        # example_custom_strategy()
        # example_comprehensive_reporting()
        # example_comparative_analysis()
        # example_portfolio_analysis()
        
        print("\n" + "="*70)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR] Error running examples: {str(e)}")
        raise


if __name__ == "__main__":
    # Run all examples
    run_all_examples()
    
    # Or run individual examples:
    # example_basic_analysis()
    # example_value_investing()
    # example_growth_investing()
    # example_dividend_investing()
    # example_quality_investing()
    # example_batch_screening()
    # example_custom_strategy()
    # example_comprehensive_reporting()
    # example_comparative_analysis()
    # example_portfolio_analysis()
