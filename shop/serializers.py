from rest_framework import serializers

from .models import Shop, ShopCategory

class ShopCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopCategory
        fields = [
            'id',
            'name',
            'description',
        ]


class ShopSerializer(serializers.ModelSerializer):

    categories = ShopCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = [
            'id',
            'name',
            'description',
            'categories',
            ]

class ShopNoCategoriesSerializer(ShopSerializer):
    class Meta(ShopSerializer.Meta):
        fields = [
            'id',
            'name',
            'description',
            ]