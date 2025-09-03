/**
 * Calculator JavaScript functionality
 * Brazilian Import Tax Calculator
 */

// Global variables
let currentCalculation = null;
let exchangeRateCache = null;
let ncmSearchTimeout = null;

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeCalculator();
    setupEventListeners();
    loadExchangeRate();
});

/**
 * Initialize calculator functionality
 */
function initializeCalculator() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // NCM code search
    const ncmInput = document.querySelector('input[list="ncm-suggestions"]');
    if (ncmInput) {
        ncmInput.addEventListener('input', handleNCMSearch);
        ncmInput.addEventListener('blur', handleNCMSelection);
    }

    // Form validation
    const calculationForm = document.getElementById('calculation-form');
    if (calculationForm) {
        calculationForm.addEventListener('submit', validateCalculationForm);
    }

    // Currency formatting
    setupCurrencyFormatting();

    // Auto-calculation for quick estimates
    setupAutoCalculation();

    // Keyboard shortcuts
    setupKeyboardShortcuts();
}

/**
 * Handle NCM code search
 */
function handleNCMSearch(event) {
    const query = event.target.value.trim();
    
    // Clear previous timeout
    if (ncmSearchTimeout) {
        clearTimeout(ncmSearchTimeout);
    }

    // Clear suggestions if query is too short
    if (query.length < 3) {
        clearNCMSuggestions();
        return;
    }

    // Debounce search
    ncmSearchTimeout = setTimeout(() => {
        searchNCMCodes(query);
    }, 300);
}

/**
 * Search NCM codes via API
 */
function searchNCMCodes(query) {
    const datalist = document.getElementById('ncm-suggestions');
    if (!datalist) return;

    // Show loading state
    showNCMLoading(true);

    fetch(`/api/ncm/buscar?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            showNCMLoading(false);
            populateNCMSuggestions(data);
        })
        .catch(error => {
            console.error('Error searching NCM codes:', error);
            showNCMLoading(false);
            showNotification('Erro ao buscar códigos NCM', 'warning');
        });
}

/**
 * Populate NCM suggestions
 */
function populateNCMSuggestions(ncmCodes) {
    const datalist = document.getElementById('ncm-suggestions');
    if (!datalist) return;

    // Clear existing options
    datalist.innerHTML = '';

    // Add new options
    ncmCodes.forEach(ncm => {
        const option = document.createElement('option');
        option.value = ncm.code;
        option.textContent = `${ncm.code} - ${ncm.description}`;
        datalist.appendChild(option);
    });
}

/**
 * Clear NCM suggestions
 */
function clearNCMSuggestions() {
    const datalist = document.getElementById('ncm-suggestions');
    if (datalist) {
        datalist.innerHTML = '';
    }
}

/**
 * Show/hide NCM loading state
 */
function showNCMLoading(show) {
    const infoDiv = document.getElementById('ncm-info');
    if (infoDiv) {
        if (show) {
            infoDiv.innerHTML = '<small class="text-muted">Buscando códigos NCM...</small>';
        } else {
            infoDiv.innerHTML = '';
        }
    }
}

/**
 * Handle NCM selection
 */
function handleNCMSelection(event) {
    const ncmCode = event.target.value.replace(/\D/g, '');
    
    if (ncmCode.length === 8) {
        validateNCMCode(ncmCode);
    }
}

/**
 * Validate NCM code and fetch details
 */
function validateNCMCode(ncmCode) {
    fetch(`/api/ncm/${ncmCode}`)
        .then(response => response.json())
        .then(data => {
            if (data.description) {
                showNCMInfo(data);
            } else {
                showNCMWarning();
            }
        })
        .catch(error => {
            console.error('Error validating NCM:', error);
            showNCMWarning();
        });
}

/**
 * Show NCM information
 */
function showNCMInfo(ncmData) {
    const infoDiv = document.getElementById('ncm-info');
    if (infoDiv) {
        infoDiv.innerHTML = `
            <div class="small">
                <strong>Descrição:</strong> ${ncmData.description}<br>
                <span class="text-success">
                    <i data-feather="check-circle" style="width: 14px; height: 14px;"></i>
                    NCM encontrado na base de dados
                </span>
            </div>
        `;
        feather.replace();
    }
}

/**
 * Show NCM warning
 */
function showNCMWarning() {
    const infoDiv = document.getElementById('ncm-info');
    if (infoDiv) {
        infoDiv.innerHTML = `
            <small class="text-warning">
                <i data-feather="alert-triangle" style="width: 14px; height: 14px;"></i>
                NCM não encontrado. Serão usadas alíquotas padrão.
            </small>
        `;
        feather.replace();
    }
}

/**
 * Load current exchange rate
 */
function loadExchangeRate() {
    const rateElement = document.getElementById('current-rate');
    if (!rateElement) return;

    fetch('/api/cotacao')
        .then(response => response.json())
        .then(data => {
            exchangeRateCache = data.rate;
            rateElement.textContent = data.formatted;
            updateCalculationPreview();
        })
        .catch(error => {
            console.error('Error loading exchange rate:', error);
            exchangeRateCache = 5.0;
            rateElement.textContent = 'R$ 5,00';
        });
}

/**
 * Setup currency formatting for inputs
 */
function setupCurrencyFormatting() {
    const currencyInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    
    currencyInputs.forEach(input => {
        input.addEventListener('blur', function() {
            formatCurrencyInput(this);
        });
    });
}

/**
 * Format currency input
 */
function formatCurrencyInput(input) {
    const value = parseFloat(input.value);
    if (!isNaN(value)) {
        input.value = value.toFixed(2);
    }
}

/**
 * Setup auto-calculation for quick estimates
 */
function setupAutoCalculation() {
    const triggerInputs = document.querySelectorAll('#unit_value_usd, #quantity');
    
    triggerInputs.forEach(input => {
        input.addEventListener('input', debounce(updateCalculationPreview, 500));
    });
}

/**
 * Update calculation preview
 */
function updateCalculationPreview() {
    const unitValue = parseFloat(document.getElementById('unit_value_usd')?.value) || 0;
    const quantity = parseInt(document.getElementById('quantity')?.value) || 1;
    const rate = exchangeRateCache || 5.0;
    
    if (unitValue > 0) {
        const fobUSD = unitValue * quantity;
        const fobBRL = fobUSD * rate;
        
        // Simple estimate (basic taxes)
        const estimatedTaxes = fobBRL * 0.6; // Rough estimate
        const estimatedTotal = fobBRL + estimatedTaxes;
        
        updatePreviewDisplay(fobBRL, estimatedTaxes, estimatedTotal);
    }
}

/**
 * Update preview display
 */
function updatePreviewDisplay(fobBRL, taxes, total) {
    // This would update a preview section if it exists
    const previewSection = document.getElementById('calculation-preview');
    if (previewSection) {
        previewSection.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h6 class="card-title">Estimativa Rápida</h6>
                    <div class="row">
                        <div class="col-4 text-center">
                            <small class="text-muted">Valor FOB</small>
                            <div class="fw-bold">R$ ${formatCurrency(fobBRL)}</div>
                        </div>
                        <div class="col-4 text-center">
                            <small class="text-muted">Impostos (est.)</small>
                            <div class="fw-bold text-warning">R$ ${formatCurrency(taxes)}</div>
                        </div>
                        <div class="col-4 text-center">
                            <small class="text-muted">Total (est.)</small>
                            <div class="fw-bold text-success">R$ ${formatCurrency(total)}</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
}

/**
 * Validate calculation form
 */
function validateCalculationForm(event) {
    const form = event.target;
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    // Clear previous validation states
    requiredFields.forEach(field => {
        field.classList.remove('is-invalid');
    });

    // Validate each required field
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        }
    });

    // Validate NCM code format
    const ncmInput = document.querySelector('input[list="ncm-suggestions"]');
    if (ncmInput) {
        const ncmCode = ncmInput.value.replace(/\D/g, '');
        if (ncmCode.length !== 8) {
            ncmInput.classList.add('is-invalid');
            isValid = false;
            showNotification('Código NCM deve ter 8 dígitos', 'danger');
        }
    }

    // Validate numeric fields
    const numericFields = form.querySelectorAll('input[type="number"]');
    numericFields.forEach(field => {
        const value = parseFloat(field.value);
        if (field.hasAttribute('required') && (isNaN(value) || value <= 0)) {
            field.classList.add('is-invalid');
            isValid = false;
        }
    });

    if (!isValid) {
        event.preventDefault();
        showNotification('Por favor, corrija os campos marcados em vermelho', 'danger');
        return false;
    }

    // Show loading state
    showLoadingOverlay(true);
    return true;
}

/**
 * Setup keyboard shortcuts
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(event) {
        // Ctrl+N for new calculation
        if (event.ctrlKey && event.key === 'n') {
            event.preventDefault();
            window.location.href = '/nova-analise';
        }
        
        // Ctrl+H for history
        if (event.ctrlKey && event.key === 'h') {
            event.preventDefault();
            window.location.href = '/historico';
        }
        
        // Ctrl+S for save scenario (if on results page)
        if (event.ctrlKey && event.key === 's' && document.getElementById('saveScenarioModal')) {
            event.preventDefault();
            new bootstrap.Modal(document.getElementById('saveScenarioModal')).show();
        }
    });
}

/**
 * Show loading overlay
 */
function showLoadingOverlay(show) {
    const overlay = document.getElementById('loading-overlay');
    
    if (show) {
        if (!overlay) {
            const loadingHTML = `
                <div id="loading-overlay" class="loading-overlay">
                    <div class="loading-spinner"></div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', loadingHTML);
        }
    } else {
        if (overlay) {
            overlay.remove();
        }
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info', duration = 5000) {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999; max-width: 400px;" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', alertHTML);
    
    // Auto-dismiss after duration
    setTimeout(() => {
        const alert = document.querySelector('.alert:last-of-type');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, duration);
}

/**
 * Format currency for display
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Copy to clipboard utility
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copiado para a área de transferência', 'success', 2000);
    }).catch(err => {
        console.error('Error copying to clipboard:', err);
        showNotification('Erro ao copiar para área de transferência', 'danger');
    });
}

/**
 * Export calculation to PDF (placeholder)
 */
function exportToPDF() {
    showNotification('Função de exportação em desenvolvimento', 'info');
}

/**
 * Print calculation
 */
function printCalculation() {
    window.print();
}

/**
 * Share calculation (if Web Share API is supported)
 */
function shareCalculation() {
    if (navigator.share) {
        navigator.share({
            title: 'Cálculo de Importação',
            text: 'Confira este cálculo de importação',
            url: window.location.href
        }).catch(err => {
            console.error('Error sharing:', err);
        });
    } else {
        // Fallback: copy URL to clipboard
        copyToClipboard(window.location.href);
    }
}

/**
 * Initialize charts (if Chart.js is available)
 */
function initializeCharts() {
    // Tax breakdown chart
    const taxChartCanvas = document.getElementById('taxChart');
    if (taxChartCanvas && typeof Chart !== 'undefined') {
        // Chart initialization would go here
        // This is handled in the template for now
    }
    
    // Exchange rate history chart
    const rateChartCanvas = document.getElementById('rateChart');
    if (rateChartCanvas && typeof Chart !== 'undefined') {
        loadExchangeRateHistory();
    }
}

/**
 * Load exchange rate history for charts
 */
function loadExchangeRateHistory() {
    fetch('/api/cotacao/historico')
        .then(response => response.json())
        .then(data => {
            createExchangeRateChart(data);
        })
        .catch(error => {
            console.error('Error loading exchange rate history:', error);
        });
}

/**
 * Create exchange rate chart
 */
function createExchangeRateChart(data) {
    const ctx = document.getElementById('rateChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'USD/BRL',
                data: Object.values(data),
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Histórico da Cotação USD/BRL'
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toFixed(4);
                        }
                    }
                }
            }
        }
    });
}

/**
 * Utility functions for form handling
 */
const FormUtils = {
    /**
     * Serialize form data to object
     */
    serializeForm: function(form) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            if (data[key]) {
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        }
        
        return data;
    },

    /**
     * Reset form and clear validation states
     */
    resetForm: function(form) {
        form.reset();
        form.querySelectorAll('.is-invalid').forEach(field => {
            field.classList.remove('is-invalid');
        });
        form.querySelectorAll('.is-valid').forEach(field => {
            field.classList.remove('is-valid');
        });
    }
};

// Export for use in other scripts
window.Calculator = {
    showNotification,
    formatCurrency,
    copyToClipboard,
    exportToPDF,
    printCalculation,
    shareCalculation,
    FormUtils
};
