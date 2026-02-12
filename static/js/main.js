// Cinema Management System - Main JavaScript

// Initialize tooltips and popovers (Bootstrap)
document.addEventListener('DOMContentLoaded', function() {
    // Tooltip
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popover
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
    }
    form.classList.add('was-validated');
}

// Show loading spinner
function showLoadingSpinner(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    }
}

// Format currency
function formatCurrency(amount) {
    return '₱' + parseFloat(amount).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// CSRF Token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Fetch with CSRF token
async function fetchWithCSRF(url, options = {}) {
    const csrftoken = getCookie('csrftoken');
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };
    
    if (csrftoken) {
        headers['X-CSRFToken'] = csrftoken;
    }
    
    return fetch(url, {
        ...options,
        headers: headers,
    });
}

// Auto-hide alerts
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Smooth page transitions
document.addEventListener('DOMContentLoaded', function() {
    document.documentElement.style.scrollBehavior = 'smooth';
});

// Handle responsive image loading
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        images.forEach(img => imageObserver.observe(img));
    } else {
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', lazyLoadImages);

// Debug mode logging
const debugMode = false;
function debug(message, data) {
    if (debugMode) {
        console.log(`[DEBUG] ${message}`, data);
    }
}
