from django.contrib import admin
from .models import AuctionItem, Bid, Notification


# Register your models here.
@admin.register(AuctionItem)
class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_price', 'current_price', 'auction_end_date', 'is_active', 'created_by')
    list_filter = ('auction_end_date', 'created_by')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction_item', 'user', 'amount', 'bid_time')
    list_filter = ('bid_time', 'user')
    search_fields = ('auction_item__title', 'user__username')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'message')
