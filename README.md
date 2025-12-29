# Stock Screener

A comprehensive Python-based stock screening tool designed to help investors identify potential investment opportunities based on fundamental analysis metrics, technical indicators, and customizable screening rules.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Screening Metrics](#screening-metrics)
- [Rules of Thumb](#rules-of-thumb)
- [Usage Guide](#usage-guide)
- [Methodology](#methodology)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Overview

Stock Screener is a powerful tool for identifying stocks that meet specific financial criteria. Whether you're a day trader looking for technical setups, a value investor hunting for undervalued companies, or a growth investor seeking high-potential stocks, this screener provides the flexibility to implement your investment strategy.

The tool combines fundamental analysis metrics with technical indicators to provide a holistic view of potential investment opportunities.

## Features

- **Fundamental Analysis Metrics**: P/E ratio, P/B ratio, ROE, ROA, debt-to-equity, dividend yield, and more
- **Technical Indicators**: Moving averages, RSI, MACD, Bollinger Bands, volume analysis
- **Customizable Screening Rules**: Create screening strategies tailored to your investment style
- **Multi-timeframe Analysis**: Analyze stocks across different time periods
- **Batch Screening**: Screen multiple stocks simultaneously
- **Export Capabilities**: Export results to CSV, JSON, or Excel
- **Real-time Data Integration**: Fetch current market data from reliable sources
- **Backtesting Support**: Test your screening strategies against historical data

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Amruth2105/stock-screener.git
cd stock-screener
```

### Step 2: Create a Virtual Environment

```bash
# On macOS and Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys (Optional)

Some features may require API keys for data providers:

```bash
# Create a .env file in the root directory
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

## Quick Start

### Basic Stock Screening

```python
from stock_screener import StockScreener

# Initialize the screener
screener = StockScreener()

# Define screening criteria
criteria = {
    'pe_ratio': {'min': 5, 'max': 20},
    'pb_ratio': {'min': 0.5, 'max': 3},
    'roc': {'min': 0.15},
    'debt_to_equity': {'max': 1.5},
    'dividend_yield': {'min': 0.02}
}

# Run screening
results = screener.screen(criteria)

# Display results
for stock in results:
    print(f"{stock['symbol']}: P/E={stock['pe_ratio']:.2f}, ROE={stock['roe']:.2%}")
```

### Screening with Technical Indicators

```python
# Add technical screening criteria
technical_criteria = {
    'price_above_sma_200': True,
    'rsi': {'min': 30, 'max': 70},
    'volume_above_avg': True,
    'macd_bullish': True
}

results = screener.screen(fundamental_criteria=criteria, technical_criteria=technical_criteria)
```

## Screening Metrics

### Fundamental Analysis Metrics

#### Valuation Metrics

| Metric | Symbol | Description | Typical Range | Interpretation |
|--------|--------|-------------|----------------|-----------------|
| **Price-to-Earnings Ratio** | P/E | Stock price divided by annual earnings per share | 10-25 | Lower = undervalued (may indicate quality); Higher = growth premium |
| **Price-to-Book Ratio** | P/B | Stock price divided by book value per share | 1-5 | Lower = potential value opportunity; Higher = growth expected |
| **Price-to-Sales Ratio** | P/S | Stock price divided by revenue per share | 0.5-3 | More stable than P/E; useful for unprofitable companies |
| **PEG Ratio** | PEG | P/E ratio divided by earnings growth rate | <1 | <1 suggests undervalued relative to growth |
| **EV/EBITDA** | EV/EBITDA | Enterprise value to EBITDA multiple | 8-15 | Useful for comparing companies with different capital structures |

#### Profitability Metrics

| Metric | Symbol | Description | Typical Range | Interpretation |
|--------|--------|-------------|----------------|-----------------|
| **Return on Equity** | ROE | Net income divided by shareholder equity | >15% | Higher = better use of shareholder capital |
| **Return on Assets** | ROA | Net income divided by total assets | >5% | Higher = more efficient asset utilization |
| **Return on Invested Capital** | ROIC | NOPAT divided by invested capital | >10% | Higher = strong competitive advantage |
| **Profit Margin** | PM | Net income divided by revenue | >10% | Higher = better pricing power and cost control |
| **Operating Margin** | OM | Operating income divided by revenue | >15% | Higher = operational efficiency |

#### Financial Health Metrics

| Metric | Symbol | Description | Typical Range | Interpretation |
|--------|--------|-------------|----------------|-----------------|
| **Debt-to-Equity Ratio** | D/E | Total debt divided by shareholders' equity | <1.5 | Lower = less financial leverage and risk |
| **Current Ratio** | CR | Current assets divided by current liabilities | 1.5-3 | 1.5-2 is healthy; <1 suggests liquidity issues |
| **Quick Ratio** | QR | (Current assets - inventory) / current liabilities | >1 | >1 indicates strong short-term liquidity |
| **Debt-to-Assets** | DA | Total debt divided by total assets | <0.6 | Lower = better financial stability |
| **Interest Coverage** | IC | EBIT divided by interest expense | >3 | Higher = better ability to service debt |

#### Growth Metrics

| Metric | Symbol | Description | Typical Range | Interpretation |
|--------|--------|-------------|----------------|-----------------|
| **Revenue Growth** | RG | Year-over-year revenue increase | >10% | Higher = expanding business |
| **Earnings Growth** | EG | Year-over-year earnings increase | >15% | Higher = improving profitability |
| **Free Cash Flow Growth** | FCFG | Year-over-year FCF increase | >10% | Higher = sustainable cash generation |
| **Book Value Growth** | BVG | Year-over-year equity increase | >10% | Higher = increasing shareholder value |

#### Dividend Metrics

| Metric | Symbol | Description | Typical Range | Interpretation |
|--------|--------|-------------|----------------|-----------------|
| **Dividend Yield** | DY | Annual dividend per share / stock price | 2-5% | Higher = income; verify sustainability |
| **Dividend Payout Ratio** | DPR | Dividends per share / earnings per share | <60% | <60% suggests sustainable dividend |
| **Dividend Growth Rate** | DGR | Year-over-year dividend increase | >5% | Higher = growing income |

#### Cash Flow Metrics

| Metric | Symbol | Description | Typical Range | Interpretation |
|--------|--------|-------------|----------------|-----------------|
| **Free Cash Flow** | FCF | Operating cash flow - capital expenditures | Positive | Positive = true earnings; available for dividends/debt |
| **Operating Cash Flow** | OCF | Cash generated from operations | Positive | Higher = quality earnings |
| **FCF Margin** | FCFM | Free cash flow divided by revenue | >10% | Higher = strong cash generation |

### Technical Analysis Metrics

#### Trend Indicators

| Indicator | Parameters | Interpretation |
|-----------|------------|-----------------|
| **Simple Moving Average (SMA)** | 20, 50, 200 | Price above MA = uptrend; below = downtrend |
| **Exponential Moving Average (EMA)** | 12, 26 | Faster response to price changes; useful for trend confirmation |
| **MACD** | 12, 26, 9 | Bullish when MACD > signal line and histogram positive |

#### Momentum Indicators

| Indicator | Range | Interpretation |
|-----------|-------|-----------------|
| **Relative Strength Index (RSI)** | 0-100 | <30 oversold; >70 overbought; 40-60 neutral |
| **Stochastic Oscillator** | 0-100 | <20 oversold; >80 overbought |
| **Rate of Change (ROC)** | Unbounded | Positive = uptrend; negative = downtrend |

#### Volatility Indicators

| Indicator | Parameters | Interpretation |
|-----------|-----------|-----------------|
| **Bollinger Bands** | 20, 2 | Price near upper band = overbought; lower = oversold |
| **Average True Range (ATR)** | 14 | Higher = more volatility; useful for position sizing |

#### Volume Indicators

| Indicator | Parameters | Interpretation |
|-----------|-----------|-----------------|
| **Volume Trend** | 20-day average | Volume above average confirms trend moves |
| **On-Balance Volume (OBV)** | Cumulative | Rising = accumulation; falling = distribution |
| **Volume Rate of Change** | 10-day period | Increasing = growing interest |

## Rules of Thumb

### Value Investing Strategy

**Goal**: Find undervalued, profitable companies with strong balance sheets

**Screening Criteria**:
- P/E Ratio: < 15 (or below market average)
- P/B Ratio: < 1.5
- PEG Ratio: < 1.0
- ROE: > 15%
- Debt-to-Equity: < 1.0
- Dividend Yield: > 2%
- Current Ratio: > 1.5

**Additional Checks**:
- Earnings growth should be steady (>5% annually)
- Free cash flow should be positive and growing
- No significant lawsuits or regulatory issues
- Insider ownership should be reasonable (>5%)

### Growth Investing Strategy

**Goal**: Identify fast-growing companies with strong future potential

**Screening Criteria**:
- PEG Ratio: < 1.5
- Revenue Growth: > 20% (YoY)
- Earnings Growth: > 25% (YoY)
- ROE: > 20%
- Debt-to-Equity: < 1.5
- Free Cash Flow: Positive
- P/E Ratio: < 50 (relative to growth)

**Additional Checks**:
- Market opportunity should be expanding
- Competitive advantages (moat) should be evident
- Management quality and track record
- R&D spending should be appropriate for industry

### Dividend Growth Strategy

**Goal**: Find companies with sustainable and growing dividends

**Screening Criteria**:
- Dividend Yield: 2-5%
- Dividend Payout Ratio: < 60%
- Dividend Growth Rate: > 5% (over 10 years)
- P/E Ratio: < 25
- ROE: > 15%
- Debt-to-Equity: < 1.5
- Current Ratio: > 1.5

**Additional Checks**:
- Consistent dividend increases for 10+ years (Dividend Aristocrats)
- Strong and predictable cash flows
- Industry should be stable and mature
- Recession-resistant business model

### Technical Trading Strategy

**Goal**: Identify stocks with strong technical setups for short-term trading

**Screening Criteria**:
- Price above 200-day SMA (uptrend)
- Price above 50-day SMA (intermediate trend)
- RSI between 40-70 (not overbought)
- Volume above 20-day average (confirmation)
- MACD bullish (MACD > signal line)

**Additional Checks**:
- Support and resistance levels should be clear
- Average daily volume > 1M shares (liquidity)
- No earnings announcements in next few days
- Sector trend should be favorable

### Quality at Reasonable Price (GARP)

**Goal**: Combine growth and value characteristics

**Screening Criteria**:
- P/E Ratio: < 25
- PEG Ratio: < 1.2
- Revenue Growth: > 15%
- Earnings Growth: > 15%
- ROE: > 15%
- Debt-to-Equity: < 1.5
- Free Cash Flow: Positive and growing

**Additional Checks**:
- Management should have skin in the game
- Competitive advantages should be sustainable
- Market position should be strong
- Balance sheet should be healthy

## Usage Guide

### Configuration File

Create a `config.json` file to define your screening parameters:

```json
{
  "screening_profiles": {
    "value_stock": {
      "pe_ratio": {"min": 5, "max": 15},
      "pb_ratio": {"min": 0.5, "max": 1.5},
      "roe": {"min": 0.15},
      "debt_to_equity": {"max": 1.0},
      "dividend_yield": {"min": 0.02}
    },
    "growth_stock": {
      "peg_ratio": {"max": 1.5},
      "revenue_growth": {"min": 0.20},
      "earnings_growth": {"min": 0.25},
      "roe": {"min": 0.20}
    },
    "dividend_aristocrat": {
      "dividend_yield": {"min": 0.02, "max": 0.05},
      "payout_ratio": {"max": 0.60},
      "dividend_growth_10y": {"min": 0.05},
      "roe": {"min": 0.15}
    }
  }
}
```

### Running Different Screening Strategies

#### Screening a Single Stock

```python
from stock_screener import StockScreener

screener = StockScreener()
stock_analysis = screener.analyze_stock('AAPL')

print(f"Stock: {stock_analysis['symbol']}")
print(f"P/E Ratio: {stock_analysis['pe_ratio']:.2f}")
print(f"ROE: {stock_analysis['roe']:.2%}")
print(f"Debt-to-Equity: {stock_analysis['debt_to_equity']:.2f}")
```

#### Screening from a Watchlist

```python
watchlist = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
screener = StockScreener()

results = screener.screen_list(
    stocks=watchlist,
    profile='value_stock',
    config_file='config.json'
)

# Display results sorted by P/E ratio
for stock in sorted(results, key=lambda x: x['pe_ratio']):
    print(f"{stock['symbol']}: P/E={stock['pe_ratio']:.2f}")
```

#### Screening an Entire Index

```python
# Screen all S&P 500 stocks
results = screener.screen_index(
    index='SPY',
    profile='growth_stock',
    min_market_cap=1e9  # Minimum $1B market cap
)

print(f"Found {len(results)} stocks matching criteria")
```

### Exporting Results

```python
# Export to CSV
screener.export_results(results, format='csv', filename='screening_results.csv')

# Export to Excel with formatting
screener.export_results(results, format='excel', filename='screening_results.xlsx')

# Export to JSON
screener.export_results(results, format='json', filename='screening_results.json')
```

### Scheduling Regular Screens

```python
from stock_screener import ScheduledScreener
import schedule

scheduled_screener = ScheduledScreener()

# Run screening daily at 4 PM (after market close)
schedule.every().day.at("16:00").do(
    scheduled_screener.run_screen,
    profile='value_stock',
    output_file='daily_results.csv'
)

while True:
    schedule.run_pending()
```

## Methodology

### Data Collection

The stock screener collects data from multiple reliable sources:

1. **Fundamental Data**: Financial statements, earnings reports, balance sheets
2. **Market Data**: Stock prices, volume, market capitalization
3. **Technical Data**: Price history, technical indicators
4. **Corporate Actions**: Splits, dividends, earnings dates

**Data Sources**:
- Yahoo Finance API
- Alpha Vantage
- IEX Cloud
- SEC EDGAR (for detailed fundamentals)
- Custom data feeds (configurable)

### Metric Calculations

All metrics are calculated according to standard financial definitions:

- **Ratios**: Calculated from latest quarterly or annual data
- **Growth Rates**: Calculated year-over-year where applicable
- **Technical Indicators**: Calculated using standard formulas with configurable periods
- **Averages**: Simple or exponential as specified

### Data Quality Assurance

- All data is validated for accuracy and completeness
- Missing values are handled according to configurable policies
- Outliers are flagged for manual review
- Data freshness is monitored and logged

### Scoring System (Optional)

Stocks can be ranked using a composite score:

```
Score = Σ(Weight_i × Normalized_Metric_i)

Where:
- Each metric is normalized to 0-100 scale
- Weights reflect importance in your strategy
- Higher score = better fit with criteria
```

### Filtering Process

1. **Initial Filter**: Apply minimum data quality standards
2. **Hard Filters**: Apply strict pass/fail criteria
3. **Soft Filters**: Apply ranking-based criteria
4. **Final Review**: Manual validation of results

### Backtesting

Test screening rules against historical data:

```python
backtester = screener.create_backtester()

results = backtester.test(
    start_date='2020-01-01',
    end_date='2023-12-31',
    profile='value_stock',
    rebalance_frequency='quarterly'
)

print(f"Total Return: {results['total_return']:.2%}")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
```

## Configuration

### Environment Variables

```bash
# Data provider settings
YAHOO_FINANCE_API_KEY=your_key
ALPHA_VANTAGE_API_KEY=your_key
IEX_CLOUD_API_KEY=your_key

# Output settings
OUTPUT_FORMAT=csv  # csv, json, excel
OUTPUT_DIR=./results

# Performance settings
MAX_WORKERS=4  # Parallel processing threads
CACHE_ENABLED=true
CACHE_TTL=3600  # Cache time in seconds

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/screener.log
```

### Customizing Screening Profiles

Extend the provided strategies or create your own:

```python
custom_criteria = {
    'fundamental': {
        'pe_ratio': {'min': 10, 'max': 20},
        'roe': {'min': 0.18},
        'fcf_yield': {'min': 0.05},
        'net_margin': {'min': 0.10}
    },
    'technical': {
        'price_above_sma_50': True,
        'rsi_15_min': 35,
        'rsi_15_max': 65
    },
    'filters': {
        'min_market_cap': 1e9,
        'min_price': 5,
        'min_volume': 500000
    }
}

results = screener.screen(custom_criteria)
```

## API Reference

### Core Classes

#### StockScreener

Main class for stock screening operations.

```python
class StockScreener:
    def __init__(self, data_provider='yahoo', cache=True):
        """Initialize the screener."""
    
    def screen(self, criteria, limit=None):
        """Screen stocks based on criteria."""
    
    def analyze_stock(self, symbol):
        """Get detailed analysis for a single stock."""
    
    def screen_index(self, index, profile=None, limit=None):
        """Screen all stocks in an index."""
    
    def export_results(self, results, format, filename):
        """Export screening results."""
```

#### BacktestEngine

For historical analysis of screening strategies.

```python
class BacktestEngine:
    def test(self, start_date, end_date, profile, rebalance_freq):
        """Run backtest on historical data."""
    
    def get_statistics(self):
        """Get backtest statistics."""
```

### Configuration Methods

```python
screener.load_config(filepath)           # Load configuration file
screener.set_criteria(criteria_dict)     # Set screening criteria programmatically
screener.use_profile(profile_name)       # Use a predefined profile
```

## Examples

### Example 1: Find Value Stocks with Growing Dividends

```python
from stock_screener import StockScreener

screener = StockScreener()

criteria = {
    'pe_ratio': {'max': 15},
    'pb_ratio': {'max': 1.5},
    'roe': {'min': 0.15},
    'dividend_yield': {'min': 0.03},
    'payout_ratio': {'max': 0.60},
    'debt_to_equity': {'max': 1.0}
}

results = screener.screen(criteria)
screener.export_results(results, 'csv', 'dividend_value_stocks.csv')
```

### Example 2: Find Emerging Growth Stocks

```python
criteria = {
    'revenue_growth': {'min': 0.25},
    'earnings_growth': {'min': 0.30},
    'peg_ratio': {'max': 1.5},
    'roe': {'min': 0.20},
    'debt_to_equity': {'max': 1.2},
    'market_cap': {'min': 500e6, 'max': 50e9}  # Mid-cap
}

results = screener.screen(criteria)
```

### Example 3: Momentum Trading Screen

```python
criteria = {
    'technical': {
        'price_above_sma_200': True,
        'price_above_sma_50': True,
        'rsi': {'min': 50, 'max': 80},
        'volume_ratio': {'min': 1.5},  # 50% above average
        'macd_bullish': True
    },
    'filters': {
        'min_volume': 1000000,
        'price_above': 5
    }
}

results = screener.screen(criteria)
```

### Example 4: Quality Screener (GARP Style)

```python
criteria = {
    'pe_ratio': {'min': 10, 'max': 25},
    'peg_ratio': {'max': 1.2},
    'revenue_growth': {'min': 0.15},
    'earnings_growth': {'min': 0.15},
    'roe': {'min': 0.15},
    'fcf_yield': {'min': 0.05},
    'debt_to_equity': {'max': 1.5},
    'insider_ownership': {'min': 0.05}
}

results = screener.screen(criteria)
```

## Contributing

We welcome contributions to improve the stock screener! Please follow these guidelines:

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Areas for Contribution

- Additional screening metrics
- New data providers
- Performance optimizations
- Additional screening strategies
- Documentation improvements
- Bug fixes and testing

### Code Standards

- Follow PEP 8 style guidelines
- Include docstrings for all functions
- Add unit tests for new features
- Update documentation accordingly

## Disclaimer

**Important**: This tool is provided for educational and informational purposes only. It is not financial advice. Always do your own due diligence and consult with a financial advisor before making investment decisions. Past performance does not guarantee future results. Stock screening is not a guarantee of investment success.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions, please:

- Open an issue on GitHub
- Contact the maintainers
- Check existing documentation

## Version History

- **v1.0.0** (2025-12-29): Initial release with comprehensive screening metrics and strategies

## Additional Resources

- [Investopedia - Stock Screening](https://www.investopedia.com/terms/s/stockscreener.asp)
- [Financial Ratio Analysis Guide](https://www.investopedia.com/financial-term-dictionary-4771218)
- [Technical Analysis Basics](https://www.investopedia.com/technical-analysis-4689657)
- [SEC EDGAR Database](https://www.sec.gov/cgi-bin/browse-edgar)

---

**Last Updated**: 2025-12-29

For the latest updates and documentation, visit the [GitHub repository](https://github.com/Amruth2105/stock-screener)
