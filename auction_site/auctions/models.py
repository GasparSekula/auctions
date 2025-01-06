import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class AuctionItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="auction_images/", blank=True, null=True)
    auction_end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_items')
    watched_by = models.ManyToManyField(User, related_name='watchlist', blank=True)

    def __str__(self):
        return f"{self.title} - starting price: {self.starting_price} EUR"

    @property
    def is_active(self):
        """Check if the auction item is active."""
        return timezone.now() < self.auction_end_date

class Bid(models.Model):
    auction_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.user} on {self.bid_time} with amount {self.amount} EUR"

    class Meta:
        ordering = ['-bid_time']

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
