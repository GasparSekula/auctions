from rest_framework import serializers
from .models import AuctionItem

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionItem
        fields = '__all__'