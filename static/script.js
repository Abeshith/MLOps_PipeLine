// MLOps Pipeline Web Application JavaScript

// Global variables
let isFormSubmitting = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize form handlers
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePredictionSubmit);
    }

    // Initialize reset button
    const resetBtn = document.querySelector('.btn-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetForm);
    }

    // Add form validation
    addFormValidation();

    // Load initial data
    updateLastUpdatedTime();
}

function handlePredictionSubmit(e) {
    e.preventDefault();
    
    if (isFormSubmitting) return;
    
    isFormSubmitting = true;
    const submitBtn = document.getElementById('predictBtn');
    const spinner = submitBtn.querySelector('.loading-spinner');
    const btnText = submitBtn.querySelector('span');
    
    // Show loading state
    spinner.style.display = 'inline-block';
    btnText.textContent = 'Predicting...';
    submitBtn.disabled = true;
    
    // Collect form data
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    // Validate and convert data
    const processedData = processFormData(data);
    
    if (!processedData.isValid) {
        showError(processedData.error);
        resetSubmitButton(submitBtn, spinner, btnText);
        return;
    }
    
    // Make prediction request
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(processedData.data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
        } else {
            showPredictionResult(data);
        }
    })
    .catch(error => {
        console.error('Prediction error:', error);
        showError('Network error occurred. Please try again.');
    })
    .finally(() => {
        resetSubmitButton(submitBtn, spinner, btnText);
    });
}

function processFormData(formData) {
    const result = {
        isValid: true,
        error: null,
        data: {}
    };
    
    try {
        // Required fields validation
        const requiredFields = ['age', 'job', 'marital', 'education', 'housing', 'loan', 'duration', 'campaign'];
        for (const field of requiredFields) {
            if (!formData[field] || formData[field].trim() === '') {
                result.isValid = false;
                result.error = `Please fill in the ${field.replace('_', ' ')} field.`;
                return result;
            }
        }
        
        // Convert and validate numeric fields
        const numericFields = ['age', 'duration', 'campaign'];
        for (const field of numericFields) {
            const value = parseInt(formData[field]);
            if (isNaN(value) || value < 0) {
                result.isValid = false;
                result.error = `Invalid ${field} value. Please enter a positive number.`;
                return result;
            }
            result.data[field] = value;
        }
        
        // Add string fields
        const stringFields = ['job', 'marital', 'education', 'housing', 'loan'];
        for (const field of stringFields) {
            result.data[field] = formData[field];
        }
        
        // Add optional balance field
        if (formData.balance && formData.balance.trim() !== '') {
            const balance = parseInt(formData.balance);
            result.data.balance = isNaN(balance) ? 1500 : balance; // Default balance
        } else {
            result.data.balance = 1500; // Default balance
        }
        
        // Add default values for missing fields
        const defaults = {
            'default': 'no',
            'contact': 'cellular',
            'month': 'may',
            'day': 15,
            'pdays': 999,
            'previous': 0,
            'poutcome': 'nonexistent'
        };
        
        Object.assign(result.data, defaults);
        
    } catch (error) {
        result.isValid = false;
        result.error = 'Invalid form data. Please check your inputs.';
    }
    
    return result;
}

function showPredictionResult(data) {
    const resultCard = document.getElementById('resultCard');
    const resultContainer = document.getElementById('predictionResult');
    
    if (!resultCard || !resultContainer) return;
    
    const isPositive = data.prediction === 1;
    const confidence = data.confidence || data.probability;
    const confidenceLevel = data.confidence_level || getConfidenceLevel(confidence);
    
    const resultHTML = `
        <div class="prediction-result ${isPositive ? 'result-positive' : 'result-negative'}">
            <div class="result-icon">
                <i class="fas ${isPositive ? 'fa-thumbs-up' : 'fa-thumbs-down'}"></i>
            </div>
            <div class="result-title">${data.result}</div>
            <div class="result-subtitle">
                Prediction confidence: ${confidenceLevel}
            </div>
            <div class="result-metrics">
                <div class="result-metric">
                    <div class="metric-label">Subscription Probability</div>
                    <div class="metric-value">${(data.probability * 100).toFixed(1)}%</div>
                </div>
                <div class="result-metric">
                    <div class="metric-label">Confidence Score</div>
                    <div class="metric-value">${(confidence * 100).toFixed(1)}%</div>
                </div>
            </div>
            <div class="result-timestamp">
                <i class="fas fa-clock"></i>
                Predicted at ${new Date().toLocaleString()}
            </div>
        </div>
    `;
    
    resultContainer.innerHTML = resultHTML;
    resultCard.style.display = 'block';
    
    // Smooth scroll to results
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Add animation
    resultContainer.style.opacity = '0';
    resultContainer.style.transform = 'translateY(20px)';
    setTimeout(() => {
        resultContainer.style.transition = 'all 0.5s ease';
        resultContainer.style.opacity = '1';
        resultContainer.style.transform = 'translateY(0)';
    }, 100);
}

function showError(message) {
    const resultCard = document.getElementById('resultCard');
    const resultContainer = document.getElementById('predictionResult');
    
    if (!resultCard || !resultContainer) {
        alert(message);
        return;
    }
    
    const errorHTML = `
        <div class="prediction-result result-error">
            <div class="result-icon">
                <i class="fas fa-exclamation-triangle"></i>
            </div>
            <div class="result-title">Prediction Error</div>
            <div class="result-subtitle">${message}</div>
            <div class="error-suggestions">
                <h4>Suggestions:</h4>
                <ul>
                    <li>Check that all required fields are filled</li>
                    <li>Ensure numeric values are positive</li>
                    <li>Try refreshing the page if the error persists</li>
                </ul>
            </div>
        </div>
    `;
    
    resultContainer.innerHTML = errorHTML;
    resultCard.style.display = 'block';
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function resetSubmitButton(submitBtn, spinner, btnText) {
    isFormSubmitting = false;
    spinner.style.display = 'none';
    btnText.textContent = 'Predict Subscription';
    submitBtn.disabled = false;
}

function resetForm() {
    const form = document.getElementById('predictionForm');
    const resultCard = document.getElementById('resultCard');
    
    if (form) {
        form.reset();
    }
    
    if (resultCard) {
        resultCard.style.display = 'none';
    }
    
    // Reset any validation states
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.classList.remove('error', 'valid');
    });
}

function addFormValidation() {
    const form = document.getElementById('predictionForm');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input[required], select[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearValidation);
    });
}

function validateField(e) {
    const field = e.target;
    const value = field.value.trim();
    
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'This field is required');
        return false;
    }
    
    if (field.type === 'number') {
        const numValue = parseFloat(value);
        if (isNaN(numValue) || numValue < 0) {
            showFieldError(field, 'Please enter a valid positive number');
            return false;
        }
        
        // Specific validations
        if (field.name === 'age' && (numValue < 18 || numValue > 100)) {
            showFieldError(field, 'Age must be between 18 and 100');
            return false;
        }
        
        if (field.name === 'duration' && numValue > 3600) {
            showFieldError(field, 'Duration seems too long (max 1 hour)');
            return false;
        }
        
        if (field.name === 'campaign' && numValue > 50) {
            showFieldError(field, 'Campaign contacts seem excessive (max 50)');
            return false;
        }
    }
    
    clearFieldError(field);
    return true;
}

function showFieldError(field, message) {
    field.classList.add('error');
    field.classList.remove('valid');
    
    // Remove existing error message
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('error');
    field.classList.add('valid');
    
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function clearValidation(e) {
    const field = e.target;
    field.classList.remove('error');
    
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function getConfidenceLevel(confidence) {
    if (confidence > 0.8) return 'High';
    if (confidence > 0.6) return 'Medium';
    return 'Low';
}

function updateLastUpdatedTime() {
    const lastUpdateElements = document.querySelectorAll('#lastUpdate');
    lastUpdateElements.forEach(element => {
        element.textContent = new Date().toLocaleString();
    });
}

// Utility functions
function formatNumber(num, decimals = 1) {
    return Number(num).toFixed(decimals);
}

function formatPercent(num, decimals = 1) {
    return `${formatNumber(num * 100, decimals)}%`;
}

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

// Export functions for use in other scripts
window.MLOpsApp = {
    loadModelInfo,
    updateLastUpdatedTime,
    formatNumber,
    formatPercent
};

// Additional styles for validation
const validationStyles = `
.form-group input.error,
.form-group select.error {
    border-color: #ff6b6b;
    box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
}

.form-group input.valid,
.form-group select.valid {
    border-color: #4ecdc4;
    box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.1);
}

.field-error {
    color: #ff6b6b;
    font-size: 0.85rem;
    margin-top: 0.25rem;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.field-error::before {
    content: "⚠";
    font-size: 0.9rem;
}

.result-error {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    color: white;
}

.error-suggestions {
    margin-top: 1rem;
    text-align: left;
}

.error-suggestions h4 {
    margin-bottom: 0.5rem;
    font-size: 1rem;
}

.error-suggestions ul {
    margin-left: 1rem;
    opacity: 0.9;
}

.error-suggestions li {
    margin-bottom: 0.25rem;
}

.result-timestamp {
    margin-top: 1rem;
    font-size: 0.9rem;
    opacity: 0.8;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}
`;

// Inject validation styles
const styleSheet = document.createElement('style');
styleSheet.textContent = validationStyles;
document.head.appendChild(styleSheet);