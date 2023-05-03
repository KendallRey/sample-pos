
from rest_framework import serializers

from .models import OrderItem, OrderItemCancellationRequest, Rating
from shop.serializers import ShopNoCategoriesSerializer

from cart.serializers import CartItemSerializer
from account.serializers import AccountSerializer

class OrderItemSerializer(serializers.ModelSerializer):

    shop = ShopNoCategoriesSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'created_at',
            'account',
            'address',
            'cart_item',
            'shop',
            'quantity',
            'status',
            'date_placed',
            'date_out',
            'date_received',
            'date_cancelled',
        ]

class OrderItemCancellationRequestSerializer(serializers.ModelSerializer):

    account = AccountSerializer(read_only=True)
    class Meta:
        model = OrderItemCancellationRequest
        fields = [
            'id',
            'created_at',
            'account',
            'order_item',
            'reason',
            'status',
        ]

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = [
            'id',
        ]