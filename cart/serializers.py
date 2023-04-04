from rest_framework import serializers

from .models import Cart, CartItem

from item.serializers import ItemNoCategoriesSerializer

class CartItemSerializer(serializers.ModelSerializer):

    item = ItemNoCategoriesSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'created_at',
            'item',
            'quantity',
        ]

class CartSerializer(serializers.ModelSerializer):

    items_count = serializers.SerializerMethodField('get_items_count')
    total_price = serializers.SerializerMethodField('get_total_price')

    class Meta:
        model = Cart
        fields = [
            'id',
            'created_at',
            'items_count',
            'total_price',
        ]

    def get_items_count(self, obj):
        items = CartItem.objects.filter(cart = obj)
        return items.count()

    def get_total_price(self, obj):
        cart_items = CartItem.objects.filter(cart = obj)
        available_items = cart_items.filter(item__stock__gte = 1)
        total_price = 0
        for cart_item in available_items:
            calculated_price = cart_item.item.price * cart_item.quantity
            total_price += calculated_price
        return total_price
