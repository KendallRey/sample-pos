from rest_framework import serializers

from .models import Shop, ShopCategory

class ShopCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopCategory
        fields = [
            'name',
            'description',
        ]


class BaseShopSerializer(serializers.ModelSerializer):

    categories = ShopCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = [
            'id',
            'name',
            'description',
            'categories',
            ]

class ShopSerializer(BaseShopSerializer):
    pass

class ShopNoCategoriesSerializer(BaseShopSerializer):
    class Meta:
        model = Shop
        fields = [
            'id',
            'name',
            'description',
            ]