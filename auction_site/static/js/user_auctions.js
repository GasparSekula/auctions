document.getElementById('toggleClosedAuctions').addEventListener('click', function() {
    var closedAuctions = document.querySelectorAll('.closed-auction');
    closedAuctions.forEach(function(auction) {
        auction.style.display = auction.style.display === 'none' ? '' : 'none';
    });
    this.textContent = this.textContent === 'Hide Closed Auctions' ? 'Show Closed Auctions' : 'Hide Closed Auctions';
});