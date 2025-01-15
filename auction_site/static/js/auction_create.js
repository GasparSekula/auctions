document.addEventListener('DOMContentLoaded', function () {
    const auctionForm = document.getElementById('auction-form');
    const startingPriceInput = document.getElementById('starting_price');
    const auctionEndDatetimeInput = document.getElementById('auction_end_date');
    const photoPreview = document.getElementById('photoPreview');
    const imageInput = document.getElementById('image');

    // Real-time validation for starting price
    startingPriceInput.addEventListener('input', () => {
        const value = parseFloat(startingPriceInput.value);
        if (isNaN(value) || value <= 0) {
            startingPriceInput.style.color = 'red';
            startingPriceInput.setCustomValidity('Starting price must be a valid number greater than 0.');
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

        const auctionEndDatetime = new Date(auctionEndDatetimeInput.value);
        const now = new Date();
        if (!auctionEndDatetime || auctionEndDatetime <= now) {
            e.preventDefault();
            alert('Auction end date and time must be in the future.');
            return;
        }
    });
});