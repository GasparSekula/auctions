document.addEventListener('DOMContentLoaded', function () {
    const bidInput = document.getElementById('bid-amount');
    const bidError = document.getElementById('bid-error');
    const currentPrice = parseFloat(document.getElementById('current-price').textContent);

    bidInput.addEventListener('input', function () {
        const bidValue = parseFloat(bidInput.value);

        // Ensure bid amount is greater than current price
        if (bidValue <= currentPrice) {
            bidError.textContent = 'Your bid must be higher than the current price.';
            bidError.style.display = 'block';
        } else if (!/^\d{1,8}(\.\d{1,2})?$/.test(bidInput.value)) {
            // Validate the bid format (max 8 digits before decimal and 2 after)
            bidError.textContent = 'Bid amount must be a number with up to 8 digits before the decimal and 2 decimal places.';
            bidError.style.display = 'block';
        } else {
            bidError.style.display = 'none';  // Hide error if valid
        }
    });
});
