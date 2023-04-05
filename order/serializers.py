
from rest_framework import serializers

from .models import OrderItem
from shop.serializers import ShopNoCategoriesSerializer

from cart.serializers import CartItemSerializer

class BaseOrderItemSerializer(serializers.ModelSerializer):

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

class OrderItemSerializer(BaseOrderItemSerializer):

    cart_item = CartItemSerializer(read_only=True)

    pass