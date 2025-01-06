document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('toggleFormButton').addEventListener('click', function() {
        var formContainer = document.getElementById('filterFormContainer');
        if (formContainer.classList.contains('hidden')) {
            formContainer.classList.remove('hidden');
            this.textContent = 'Hide Filters and Sorting';
        } else {
            formContainer.classList.add('hidden');
            this.textContent = 'Show Filters and Sorting';
        }
    });
});

function updatePriceLabel(value) {
        document.getElementById('price-label').innerText = value;
    }