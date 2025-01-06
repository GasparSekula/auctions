document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('toggleFormButton').addEventListener('click', function () {
        var formContainer = document.getElementById('filterFormContainer');
        if (formContainer.classList.contains('hidden')) {
            formContainer.classList.remove('hidden');
            this.textContent = 'Hide Filters and Sorting';
        } else {
            formContainer.classList.add('hidden');
            this.textContent = 'Show Filters and Sorting';
        }
    });

    const filterForm = document.getElementById('filterForm');
    const minPriceInput = document.getElementById('min_price');
    const maxPriceInput = document.getElementById('max_price');
    // const startDateInput = document.getElementById('start_date');
    // const endDateInput = document.getElementById('end_date');

    filterForm.addEventListener('submit', (e) => {
        console.log('Form submission triggered.');

        // Parse input values
        const minPrice = minPriceInput.value ? parseFloat(minPriceInput.value) : null;
        const maxPrice = maxPriceInput.value ? parseFloat(maxPriceInput.value) : null;
        // const startDate = startDateInput.value ? new Date(startDateInput.value) : null;
        // const endDate = endDateInput.value ? new Date(endDateInput.value) : null;

        console.log('Parsed Values:', { minPrice, maxPrice, startDate, endDate });

        let validationErrors = [];

        // Validate min and max prices
        if (minPrice !== null && maxPrice !== null) {
            if (minPrice > maxPrice) {
                validationErrors.push('Minimum price must be less than or equal to maximum price.');
                minPriceInput.style.borderColor = 'red';
                maxPriceInput.style.borderColor = 'red';
            } else {
                minPriceInput.style.borderColor = '';
                maxPriceInput.style.borderColor = '';
            }
        }

        // Validate date range
        // if (startDate && endDate) {
        //     if (startDate > endDate) {
        //         validationErrors.push('Start date must be less than or equal to end date.');
        //         startDateInput.style.borderColor = 'red';
        //         endDateInput.style.borderColor = 'red';
        //     } else {
        //         startDateInput.style.borderColor = '';
        //         endDateInput.style.borderColor = '';
        //     }
        // }

        // If there are validation errors, prevent form submission and display errors
        if (validationErrors.length > 0) {
            e.preventDefault();
            console.error('Validation errors:', validationErrors);
            alert(validationErrors.join('\n'));
        }
    });
});
