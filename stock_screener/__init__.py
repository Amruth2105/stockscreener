"""
Stock Screener Package

A comprehensive Python-based stock screening tool for fundamental analysis.
"""

from .core import (
    StockData,
    ScreeningResult,
    ScreeningStrategy,
    MetricsCalculator,
    StockAnalyzer,
    ScreeningEngine,
    StrategyBuilder,
    batch_screen
)
from .data_provider import DataProvider, StockScreener
from .strategies import ValueStrategy, GrowthStrategy, DividendStrategy, QualityStrategy

__all__ = [
    'StockData',
    'ScreeningResult',
    'ScreeningStrategy',
    'MetricsCalculator',
    'StockAnalyzer',
    'ScreeningEngine',
    'StrategyBuilder',
    'batch_screen',
    'DataProvider',
    'StockScreener',
    'ValueStrategy',
    'GrowthStrategy',
    'DividendStrategy',
    'QualityStrategy'
]

__version__ = '1.0.0'
