// main.js - ShopEase Frontend Scripts

// Auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        document.querySelectorAll('.alert').forEach(function (alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 4000);
});

// Quantity input: prevent going below 1
document.querySelectorAll('input[type=number][name=quantity]').forEach(function (input) {
    input.addEventListener('change', function () {
        if (parseInt(this.value) < 1) this.value = 1;
    });
});

// Confirm delete modals
document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
        if (!confirm(this.dataset.confirm)) e.preventDefault();
    });
});
