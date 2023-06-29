from rest_framework import serializers

from .models import Item, ItemCategory, ItemImage
from pos.models import Base64ImageField

class ItemCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemCategory
        fields = [
            'id',
            'name',
            'description',
        ]

class ItemSerializer(serializers.ModelSerializer):

    image = Base64ImageField(required = False)
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
        
class ItemImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemImage
        fields = [
            'id',
            'item',
            'image',
        ]