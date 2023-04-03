from rest_framework import serializers

from .models import Cart, CartItem

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
        items = CartItem.objects.filter(cart = obj)
        return sum(_.price for _ in items)
