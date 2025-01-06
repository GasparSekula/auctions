document.addEventListener('DOMContentLoaded', () => {
        const bidInput = document.getElementById('bid-amount');
        const currentPrice = parseFloat(document.getElementById('current-price').innerText);
        const bidError = document.getElementById('bid-error');
        const bidForm = document.getElementById('bid-form');

        // Real-time validation
        bidInput.addEventListener('input', () => {
            const bidValue = parseFloat(bidInput.value);
            if (bidValue <= currentPrice) {
                bidError.style.display = 'block';
                bidInput.style.color = 'red';
            } else {
                bidError.style.display = 'none';
                bidInput.style.color = 'black';
            }
        });

        // Final validation on submit
        bidForm.addEventListener('submit', (e) => {
            const bidValue = parseFloat(bidInput.value);
            if (bidValue <= currentPrice) {
                e.preventDefault();
                bidError.style.display = 'block';
                bidInput.style.color = 'red';
                alert("Your bid must be higher than the current price.");
            }
        });
    });