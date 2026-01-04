"""
Stock Screener Flask API

Provides REST API endpoints for:
- Single stock analysis
- Batch stock analysis
- Strategy-based screening
- Rules of thumb evaluation
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

from stock_screener import StockScreener
from stock_screener.strategies import (
    ValueStrategy,
    GrowthStrategy,
    DividendStrategy,
    QualityStrategy,
    MomentumStrategy,
    GARPStrategy,
    SCREENING_PROFILES
)

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

screener = StockScreener()


# Serve static files
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


# API Endpoints
@app.route('/api/analyze/<symbol>')
def analyze_stock(symbol):
    """
    Analyze a single stock.
    
    Returns comprehensive analysis including all metrics and signals.
    """
    try:
        analysis = screener.analyze_stock(symbol.upper())
        return jsonify({
            'success': True,
            'data': analysis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/evaluate/<symbol>')
def evaluate_stock(symbol):
    """
    Evaluate a stock against rules of thumb.
    
    Returns detailed evaluation with scores and recommendations.
    """
    try:
        evaluation = screener.get_rules_of_thumb_evaluation(symbol.upper())
        return jsonify({
            'success': True,
            'data': evaluation
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/batch', methods=['POST'])
def batch_analyze():
    """
    Analyze multiple stocks.
    
    Request body:
    {
        "symbols": ["AAPL", "MSFT", "GOOGL"],
        "metrics": ["pe_ratio", "roe", "dividend_yield"]  // optional
    }
    """
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        metrics = data.get('metrics', None)
        
        if not symbols:
            return jsonify({
                'success': False,
                'error': 'No symbols provided'
            }), 400
        
        df = screener.batch_analyze(symbols, metrics)
        results = df.to_dict('records') if not df.empty else []
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/screen', methods=['POST'])
def screen_stocks():
    """
    Screen stocks based on criteria.
    
    Request body:
    {
        "symbols": ["AAPL", "MSFT", "GOOGL", "AMZN"],
        "strategy": "value",  // or "growth", "dividend", "quality", "momentum", "garp"
        "criteria": {         // optional custom criteria
            "pe_ratio": {"max": 20},
            "roe": {"min": 0.15}
        }
    }
    """
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        strategy_name = data.get('strategy', 'custom')
        custom_criteria = data.get('criteria', None)
        
        if not symbols:
            return jsonify({
                'success': False,
                'error': 'No symbols provided'
            }), 400
        
        # Get strategy
        strategy_map = {
            'value': ValueStrategy,
            'growth': GrowthStrategy,
            'dividend': DividendStrategy,
            'quality': QualityStrategy,
            'momentum': MomentumStrategy,
            'garp': GARPStrategy
        }
        
        if strategy_name in strategy_map:
            strategy = strategy_map[strategy_name](custom_criteria)
        elif custom_criteria:
            strategy = None  # Will use custom_criteria directly
        else:
            return jsonify({
                'success': False,
                'error': f'Unknown strategy: {strategy_name}'
            }), 400
        
        df = screener.screen_stocks(symbols, strategy=strategy, criteria=custom_criteria)
        results = df.to_dict('records') if not df.empty else []
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results),
            'strategy': strategy_name
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/profiles')
def get_profiles():
    """
    Get available screening profiles.
    """
    return jsonify({
        'success': True,
        'data': {
            'strategies': ['value', 'growth', 'dividend', 'quality', 'momentum', 'garp'],
            'profiles': SCREENING_PROFILES
        }
    })


@app.route('/api/rules-of-thumb')
def get_rules_of_thumb():
    """
    Get all rules of thumb for reference.
    """
    rules = {
        'pe_ratio': {
            'name': 'P/E Ratio',
            'rule': '15-20 is reasonable',
            'low': '<15 may indicate undervaluation',
            'high': '>25 may indicate overvaluation',
            'tip': 'Compare to peers and industry average'
        },
        'debt_to_equity': {
            'name': 'Debt-to-Equity',
            'rule': '<1 is safer',
            'moderate': '1-2 is moderate',
            'high': '>2 is high risk',
            'tip': 'Check cash flow to ensure debt can be serviced'
        },
        'current_ratio': {
            'name': 'Current Ratio',
            'rule': '2:1 is healthy',
            'low': '<1 indicates liquidity issues',
            'high': '>3 may indicate inefficient asset use',
            'tip': 'Too high might suggest inefficient operations'
        },
        'roe': {
            'name': 'Return on Equity',
            'rule': '15%+ is good',
            'excellent': '>20% is excellent',
            'poor': '<10% is concerning',
            'tip': 'Compare to industry peers'
        },
        'payout_ratio': {
            'name': 'Dividend Payout Ratio',
            'rule': '<60% is sustainable',
            'high': '>80% may limit growth',
            'tip': 'High payout leaves less for reinvestment'
        },
        'pb_ratio': {
            'name': 'P/B Ratio',
            'rule': '<1 may indicate undervaluation',
            'fair': '1-3 is fair value',
            'tip': 'Better metric for asset-heavy industries'
        },
        'free_cash_flow': {
            'name': 'Free Cash Flow',
            'rule': 'Should be positive and growing',
            'tip': 'More reliable than earnings in some cases'
        },
        'revenue_growth': {
            'name': 'Revenue Growth',
            'rule': 'Look for consistent growth over 5-10 years',
            'tip': 'Sudden jumps may indicate inconsistent performance'
        },
        'eps_growth': {
            'name': 'EPS Growth',
            'rule': 'Should grow in tandem with revenue',
            'tip': 'Ensure growth is not just from cost-cutting'
        }
    }
    
    return jsonify({
        'success': True,
        'data': rules
    })


@app.route('/api/popular-stocks')
def get_popular_stocks():
    """
    Get a list of popular stocks for quick screening.
    """
    stocks = {
        'tech_giants': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA'],
        'dividend_aristocrats': ['JNJ', 'PG', 'KO', 'PEP', 'MCD', 'WMT'],
        'financials': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'V', 'MA'],
        'healthcare': ['UNH', 'JNJ', 'PFE', 'MRK', 'ABBV', 'LLY'],
        'energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG'],
        'consumer': ['AMZN', 'HD', 'NKE', 'SBUX', 'TGT', 'COST']
    }
    
    return jsonify({
        'success': True,
        'data': stocks
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
