/**
 * Stock Screener - Interactive Frontend Logic
 * Connects to the Flask API and manages the UI state
 */

const API_BASE_URL = '/api';

// State Management
const state = {
    stocks: [],
    currentStock: null,
    loading: false,
    rulesOfThumb: null,
    popularStocks: null
};

// DOM Elements
const elements = {
    searchInput: document.getElementById('search-input'),
    searchBtn: document.getElementById('search-btn'),
    stocksGrid: document.getElementById('stocks-grid'),
    filterForm: document.getElementById('filter-form'),
    loadingIndicator: document.getElementById('loading-indicator'),
    modal: document.getElementById('modal'),
    modalContent: document.getElementById('modal-body'),
    closeModal: document.getElementById('close-modal'),
    strategyChips: document.querySelectorAll('.chip')
};

// Initialize
async function init() {
    await fetchReferenceData();
    setupEventListeners();
    // Load some initial stocks
    await screenStocks('value');
}

// Fetch constant data from API
async function fetchReferenceData() {
    try {
        const [rulesRes, popularRes] = await Promise.all([
            fetch(`${API_BASE_URL}/rules-of-thumb`),
            fetch(`${API_BASE_URL}/popular-stocks`)
        ]);

        const rulesData = await rulesRes.json();
        const popularData = await popularRes.json();

        if (rulesData.success) state.rulesOfThumb = rulesData.data;
        if (popularData.success) state.popularStocks = popularData.data;

        renderRulesExplanation();
    } catch (error) {
        console.error('Error fetching reference data:', error);
    }
}

// Setup Event Listeners
function setupEventListeners() {
    elements.searchBtn.addEventListener('click', () => {
        const symbol = elements.searchInput.value.trim();
        if (symbol) analyzeStock(symbol);
    });

    elements.searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const symbol = elements.searchInput.value.trim();
            if (symbol) analyzeStock(symbol);
        }
    });

    elements.strategyChips.forEach(chip => {
        chip.addEventListener('click', () => {
            elements.strategyChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            const strategy = chip.dataset.strategy;
            screenStocks(strategy);
        });
    });

    elements.closeModal.addEventListener('click', hideModal);

    window.addEventListener('click', (e) => {
        if (e.target === elements.modal) hideModal();
    });
}

// Actions
async function analyzeStock(symbol) {
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE_URL}/analyze/${symbol}`);
        const result = await response.json();

        if (result.success) {
            state.stocks = [result.data];
            renderStocks();
            showStockDetails(symbol); // Show full evaluation for searched stock
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error('Error analyzing stock:', error);
    } finally {
        showLoading(false);
    }
}

async function screenStocks(strategy) {
    showLoading(true);
    // Use popular tech giants for initial screening if strategy is selected
    const symbols = state.popularStocks ?
        [...state.popularStocks.tech_giants, ...state.popularStocks.dividend_aristocrats] :
        ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JNJ', 'PG', 'KO'];

    try {
        const response = await fetch(`${API_BASE_URL}/screen`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbols, strategy })
        });
        const result = await response.json();

        if (result.success) {
            state.stocks = result.data;
            renderStocks();
        }
    } catch (error) {
        console.error('Error screening stocks:', error);
    } finally {
        showLoading(false);
    }
}

async function showStockDetails(symbol) {
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE_URL}/evaluate/${symbol}`);
        const result = await response.json();

        if (result.success) {
            renderEvaluationModal(result.data);
            showModal();
        }
    } catch (error) {
        console.error('Error fetching evaluation:', error);
    } finally {
        showLoading(false);
    }
}

// UI Rendering
function renderStocks() {
    if (state.stocks.length === 0) {
        elements.stocksGrid.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <p>No stocks found matching the criteria.</p>
            </div>
        `;
        return;
    }

    elements.stocksGrid.innerHTML = state.stocks.map(stock => `
        <div class="stock-card" onclick="showStockDetails('${stock.symbol}')">
            <div class="stock-header">
                <div class="stock-info">
                    <div class="stock-logo">${stock.symbol.substring(0, 2)}</div>
                    <div class="stock-name">
                        <h3>${stock.symbol}</h3>
                        <span>${stock.fundamental_strength || 'N/A'}</span>
                    </div>
                </div>
                <div class="stock-price">
                    <div class="price-value">$${stock.current_price.toFixed(2)}</div>
                    <div class="price-change ${stock.revenue_growth >= 0 ? 'positive' : 'negative'}">
                        ${stock.revenue_growth >= 0 ? '▲' : '▼'} ${(stock.revenue_growth * 100).toFixed(1)}%
                    </div>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-label">P/E Ratio</div>
                    <div class="metric-value ${getPEClass(stock.pe_ratio)}">${stock.pe_ratio ? stock.pe_ratio.toFixed(2) : 'N/A'}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">ROE</div>
                    <div class="metric-value ${stock.roe >= 0.15 ? 'good' : 'warning'}">${(stock.roe * 100).toFixed(1)}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Div Yield</div>
                    <div class="metric-value">${(stock.dividend_yield * 100).toFixed(2)}%</div>
                </div>
            </div>

            <div class="signals">
                ${stock.signals.slice(0, 3).map(s => `<span class="signal">${s.replace(/_/g, ' ')}</span>`).join('')}
                ${stock.signals.length > 3 ? `<span class="signal">+${stock.signals.length - 3} move</span>` : ''}
            </div>
        </div>
    `).join('');
}

function renderEvaluationModal(data) {
    const { symbol, evaluations, percentage, recommendation } = data;

    const scoreClass = percentage >= 80 ? 'excellent' : (percentage >= 60 ? 'good' : (percentage >= 40 ? 'moderate' : 'poor'));

    elements.modalContent.innerHTML = `
        <div class="evaluation-summary">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                <div>
                    <h2 style="font-size: 2rem; margin-bottom: 0.5rem;">${symbol} Analysis</h2>
                    <p style="color: var(--text-secondary);">Comprehensive 12-Point Rule of Thumb Evaluation</p>
                </div>
                <div style="text-align: right;">
                    <div class="score-badge ${scoreClass}" style="font-size: 1.5rem; padding: 0.5rem 1.5rem;">
                        ${percentage.toFixed(0)}% Score
                    </div>
                    <p style="margin-top: 0.5rem; font-weight: 700; color: var(--accent-purple);">${recommendation.replace(/_/g, ' ')}</p>
                </div>
            </div>

            <div class="rules-evaluation-list">
                ${evaluations.map((ev, index) => `
                    <div class="glass-card" style="margin-bottom: 1rem; padding: 1.25rem;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <div style="width: 32px; height: 32px; background: var(--primary-gradient); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold;">
                                    ${index + 1}
                                </div>
                                <div>
                                    <h4 style="font-size: 1rem;">${ev.metric}</h4>
                                    <p style="font-size: 0.75rem; color: var(--text-muted);">${ev.rule}</p>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-weight: bold; font-size: 1.1rem; color: ${ev.score >= 8 ? 'var(--accent-green)' : (ev.score >= 5 ? 'var(--accent-orange)' : 'var(--accent-red)')};">
                                    ${ev.value}
                                </div>
                                <span style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted);">${ev.status}</span>
                            </div>
                        </div>
                        <div style="font-size: 0.875rem; color: var(--text-secondary); padding-top: 0.75rem; border-top: 1px solid var(--glass-border);">
                            <span style="color: var(--accent-purple); font-weight: 600;">💡 Tip:</span> ${ev.tip}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function renderRulesExplanation() {
    const rulesGrid = document.getElementById('rules-grid');
    if (!rulesGrid || !state.rulesOfThumb) return;

    rulesGrid.innerHTML = Object.entries(state.rulesOfThumb).map(([key, rule]) => `
        <div class="rule-card">
            <div class="rule-header">
                <div class="rule-icon">
                    <span style="font-size: 1.2rem;">📈</span>
                </div>
                <div class="rule-name">${rule.name}</div>
            </div>
            <div class="rule-content">
                <p><strong>Rule:</strong> ${rule.rule}</p>
                <p class="tip"><strong>Tip:</strong> ${rule.tip}</p>
            </div>
        </div>
    `).join('');
}

// Helpers
function getPEClass(pe) {
    if (!pe) return '';
    if (pe < 15) return 'good';
    if (pe < 25) return '';
    return 'warning';
}

function showLoading(show) {
    state.loading = show;
    elements.loadingIndicator.style.display = show ? 'block' : 'none';
    if (show) {
        elements.resultsSection.style.opacity = '0.5';
    } else {
        elements.resultsSection.style.opacity = '1';
    }
}

function showModal() {
    elements.modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function hideModal() {
    elements.modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Map additional elements after DOM loads
document.addEventListener('DOMContentLoaded', () => {
    elements.resultsSection = document.getElementById('results-section');
    init();
});
