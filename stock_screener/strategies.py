"""
Strategy Classes Module

Provides strategy classes for different investment styles.
Each strategy encapsulates specific screening criteria based on investment philosophy.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class ScreeningCriteria:
    """Base criteria for stock screening"""
    pe_ratio: Dict[str, float] = None
    pb_ratio: Dict[str, float] = None
    roe: Dict[str, float] = None
    roa: Dict[str, float] = None
    debt_to_equity: Dict[str, float] = None
    current_ratio: Dict[str, float] = None
    dividend_yield: Dict[str, float] = None
    revenue_growth: Dict[str, float] = None
    earnings_growth: Dict[str, float] = None
    payout_ratio: Dict[str, float] = None
    free_cash_flow: Dict[str, float] = None


class BaseStrategy:
    """Base class for all investment strategies"""
    
    def __init__(self, name: str = "Custom", criteria: Dict = None, description: str = ""):
        self.name = name
        self.criteria = criteria or {}
        self.description = description
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"


class ValueStrategy(BaseStrategy):
    """
    Value Investing Strategy
    
    Focuses on finding undervalued stocks with:
    - Low P/E ratio (<15)
    - Low P/B ratio (<1.5)
    - Decent ROE (>10%)
    - Low debt
    - Reasonable dividend yield
    
    Rule of Thumb: Look for stocks trading below intrinsic value
    """
    
    def __init__(self, criteria: Dict = None):
        default_criteria = {
            'pe_ratio': {'max': 15},
            'pb_ratio': {'max': 1.5},
            'roe': {'min': 0.10},
            'debt_to_equity': {'max': 1.0},
            'current_ratio': {'min': 1.5}
        }
        if criteria:
            default_criteria.update(criteria)
        
        super().__init__(
            name="Value Investing",
            criteria=default_criteria,
            description="Find undervalued stocks with strong fundamentals"
        )


class GrowthStrategy(BaseStrategy):
    """
    Growth Investing Strategy
    
    Focuses on companies with high growth potential:
    - High revenue growth (>15%)
    - High earnings growth (>15%)
    - Higher P/E acceptable (15-50)
    - Strong ROE (>15%)
    
    Rule of Thumb: Growth stocks are riskier but may offer higher rewards
    """
    
    def __init__(self, criteria: Dict = None):
        default_criteria = {
            'revenue_growth': {'min': 0.15},
            'earnings_growth': {'min': 0.15},
            'pe_ratio': {'min': 15, 'max': 50},
            'roe': {'min': 0.15}
        }
        if criteria:
            default_criteria.update(criteria)
        
        super().__init__(
            name="Growth Investing",
            criteria=default_criteria,
            description="Find companies with high growth potential"
        )


class DividendStrategy(BaseStrategy):
    """
    Dividend Investing Strategy
    
    Focuses on income-generating stocks:
    - High dividend yield (>3%)
    - Sustainable payout ratio (<60%)
    - Positive free cash flow
    - Low to moderate debt
    
    Rule of Thumb: Dividend payout <60% is sustainable
    """
    
    def __init__(self, criteria: Dict = None):
        default_criteria = {
            'dividend_yield': {'min': 0.03},
            'payout_ratio': {'max': 0.70},
            'debt_to_equity': {'max': 1.0},
            'current_ratio': {'min': 1.0}
        }
        if criteria:
            default_criteria.update(criteria)
        
        super().__init__(
            name="Dividend Investing",
            criteria=default_criteria,
            description="Find stocks with attractive and sustainable dividends"
        )


class QualityStrategy(BaseStrategy):
    """
    Quality Investing Strategy
    
    Focuses on high-quality companies:
    - High ROE (>15%)
    - High ROA (>10%)
    - Low debt (<1.0 D/E)
    - Strong current ratio (>2.0)
    - Consistent performance
    
    Rule of Thumb: Quality companies withstand market downturns better
    """
    
    def __init__(self, criteria: Dict = None):
        default_criteria = {
            'roe': {'min': 0.15},
            'roa': {'min': 0.10},
            'debt_to_equity': {'max': 1.0},
            'current_ratio': {'min': 2.0},
            'interest_coverage': {'min': 5.0}
        }
        if criteria:
            default_criteria.update(criteria)
        
        super().__init__(
            name="Quality Investing",
            criteria=default_criteria,
            description="Find high-quality companies with strong fundamentals"
        )


class MomentumStrategy(BaseStrategy):
    """
    Momentum Investing Strategy
    
    Focuses on stocks with positive price and earnings momentum:
    - High earnings growth
    - Strong revenue growth
    - Positive market momentum
    
    Rule of Thumb: Momentum strategies work in trending markets
    """
    
    def __init__(self, criteria: Dict = None):
        default_criteria = {
            'earnings_growth': {'min': 0.20},
            'revenue_growth': {'min': 0.15}
        }
        if criteria:
            default_criteria.update(criteria)
        
        super().__init__(
            name="Momentum Investing",
            criteria=default_criteria,
            description="Find stocks with strong price and earnings momentum"
        )


class GARPStrategy(BaseStrategy):
    """
    Growth At a Reasonable Price (GARP) Strategy
    
    Combines growth and value:
    - Moderate P/E (10-25)
    - PEG ratio < 2
    - Decent growth (>10%)
    - Strong fundamentals
    
    Rule of Thumb: Balance growth potential with reasonable valuation
    """
    
    def __init__(self, criteria: Dict = None):
        default_criteria = {
            'pe_ratio': {'min': 10, 'max': 25},
            'earnings_growth': {'min': 0.10},
            'revenue_growth': {'min': 0.10},
            'roe': {'min': 0.12},
            'debt_to_equity': {'max': 1.5}
        }
        if criteria:
            default_criteria.update(criteria)
        
        super().__init__(
            name="GARP",
            criteria=default_criteria,
            description="Find growth stocks at reasonable prices"
        )


# Utility function to create custom strategy
def create_custom_strategy(name: str, criteria: Dict, description: str = "") -> BaseStrategy:
    """
    Create a custom screening strategy.
    
    Args:
        name: Strategy name
        criteria: Dictionary of screening criteria
        description: Optional description
        
    Returns:
        BaseStrategy instance
    """
    return BaseStrategy(name=name, criteria=criteria, description=description)


# Pre-defined screening profiles based on rules of thumb
SCREENING_PROFILES = {
    'conservative': {
        'pe_ratio': {'max': 15},
        'debt_to_equity': {'max': 0.5},
        'current_ratio': {'min': 2.0},
        'roe': {'min': 0.12},
        'dividend_yield': {'min': 0.02}
    },
    'aggressive': {
        'revenue_growth': {'min': 0.25},
        'earnings_growth': {'min': 0.25},
        'roe': {'min': 0.15}
    },
    'income': {
        'dividend_yield': {'min': 0.04},
        'payout_ratio': {'max': 0.60},
        'debt_to_equity': {'max': 1.0}
    },
    'balanced': {
        'pe_ratio': {'min': 10, 'max': 25},
        'debt_to_equity': {'max': 1.0},
        'current_ratio': {'min': 1.5},
        'roe': {'min': 0.10}
    }
}
