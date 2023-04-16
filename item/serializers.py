from rest_framework import serializers

from .models import Item, ItemCategory

class ItemCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemCategory
        fields = [
            'name',
            'description',
        ]

class ItemSerializer(serializers.ModelSerializer):

    categories = ItemCategorySerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField("get_discounted_price")
    discount_price = serializers.SerializerMethodField("get_discount_price")
    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'created_at',
            'price',
            'categories',
            'discount',
            'discounted_price',
            'discount_price',
            'image',
            ]
        
    def get_discounted_price(self, obj):
        discount_amount = (obj.discount/100) * obj.price
        return obj.price - discount_amount

    def get_discount_price(self, obj):
        return (obj.discount/100) * obj.price

class ItemNoCategoriesSerializer(ItemSerializer):

    class Meta(ItemSerializer.Meta):
        fields = [
            'id',
            'name',
            'created_at',
            'price',
            'discount',
            'discounted_price',
            'discount_price',
            ]