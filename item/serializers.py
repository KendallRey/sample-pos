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

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'created_at',
            'categories',
            'price',
            'discount',
            ]