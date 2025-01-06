document.addEventListener('DOMContentLoaded', () => {
    const auctionForm = document.getElementById('auction-form');
    const startingPriceInput = document.getElementById('starting_price');
    const endDateInput = document.getElementById('auction_end_date');
    const endTimeInput = document.getElementById('auction_end_time');
    const photoPreview = document.getElementById('photoPreview');
    const imageInput = document.getElementById('image');

    // Real-time validation for starting price
    startingPriceInput.addEventListener('input', () => {
        const value = parseFloat(startingPriceInput.value);
        if (value <= 1) {
            startingPriceInput.style.color = 'red';
            startingPriceInput.setCustomValidity('Starting price must be greater than 1.');
        } else {
            startingPriceInput.style.color = 'black';
            startingPriceInput.setCustomValidity(''); // Reset custom validity
        }
    });

    // Preview uploaded image
    imageInput.addEventListener('change', () => {
        const file = imageInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                photoPreview.src = e.target.result;
                photoPreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Final validation on form submit
    auctionForm.addEventListener('submit', (e) => {
        const startingPrice = parseFloat(startingPriceInput.value);
        if (isNaN(startingPrice) || startingPrice <= 0) {
            e.preventDefault();
            startingPriceInput.style.color = 'red';
            alert('Please enter a valid starting price greater than 0.');
            return;
        }

        const endDate = new Date(`${endDateInput.value}T${endTimeInput.value}`);
        const now = new Date();
        if (isNaN(endDate.getTime()) || endDate <= now) {
            if (endDate.toDateString() === now.toDateString() && endDate > now) {
                return;
            }
            e.preventDefault();
            alert('Auction end date and time must be in the future.');
            return;
        }
    });
});