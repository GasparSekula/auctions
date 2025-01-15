from celery import shared_task
from django.utils.timezone import now
from .models import AuctionItem, Notification, Bid


@shared_task
def notify_auction_ended():
    ended_auctions = AuctionItem.objects.filter(auction_end_date__lte=now(), is_active=True)
    for auction in ended_auctions:
        auction.is_active = False  # Mark auction as inactive
        auction.save()

        # Notify the auction winner
        winning_bid = Bid.objects.filter(auction_item=auction).order_by('-amount').first()
        if winning_bid:
            Notification.objects.create(
                user=winning_bid.user,
                message=f"Congratulations! You won the auction '{auction.title}' with a bid of {winning_bid.amount}. "
                        f"Contact the auction creator at {auction.created_by.email}."
            )

        # Notify the auction creator
        Notification.objects.create(
            user=auction.created_by,
            message=f"Your auction '{auction.title}' has ended. Winning user: {winning_bid.user.username if winning_bid else 'None'}, contact: {winning_bid.user.email if winning_bid else 'None'}."
        )
