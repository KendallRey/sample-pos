from rest_framework import serializers

from .models import Cart, CartItem, Item

from item.serializers import ItemNoCategoriesSerializer

class CartItemSerializer(serializers.ModelSerializer):

    item = ItemNoCategoriesSerializer(read_only=True)
    total_price = serializers.SerializerMethodField("get_total_price")
    total_discounted_price = serializers.SerializerMethodField("get_total_discounted_price")
    total_discount_price = serializers.SerializerMethodField("get_total_discount_price")
    class Meta:
        model = CartItem
        fields = [
            'id',
            'created_at',
            'item',
            'quantity',
            'total_price',
            'total_discounted_price',
            'total_discount_price',
        ]
    
    def get_total_price(self, obj):
        return obj.item.price * obj.quantity

    def get_total_discounted_price(self, obj):
        total_price = obj.item.price * obj.quantity
        discounted_price = total_price - (total_price * obj.item.discount/100)
        return discounted_price

    def get_total_discount_price(self, obj):
        total_price = obj.item.price * obj.quantity
        return (total_price * obj.item.discount/100)

class CartSerializer(serializers.ModelSerializer):

    items_count = serializers.SerializerMethodField('get_items_count')
    items_quantity = serializers.SerializerMethodField('get_items_quantity')
    total_price = serializers.SerializerMethodField('get_total_price')
    total_discounted_price = serializers.SerializerMethodField('get_total_discounted_price')
    total_discount_price = serializers.SerializerMethodField('get_total_discount_price')

    class Meta:
        model = Cart
        fields = [
            'id',
            'created_at',
            'items_count',
            'items_quantity',
            'total_price',
            'total_discounted_price',
            'total_discount_price',
        ]

    # total count of items
    # this is not the quantity
    def get_items_count(self, obj):
        items = CartItem.objects.filter(cart = obj)
        return items.count()

    # total count of items quantity
    def get_items_quantity(self, obj):
        cart_items = CartItem.objects.filter(cart = obj)
        total_quantity = 0
        for item in cart_items:
            total_quantity += item.quantity
        return total_quantity

    # total price of items
    # calculated with quantity
    # discount is NOT APPLIED
    def get_total_price(self, obj):
        cart_items = CartItem.objects.filter(cart = obj)
        available_items = cart_items.filter(item__stock__gte = 1)
        total_price = 0
        for cart_item in available_items:
            calculated_price = cart_item.item.price * cart_item.quantity
            total_price += calculated_price
        return total_price

    # total price of items
    # calculated with quantity
    # discount is APPLIED
    def get_total_discounted_price(self, obj):
        cart_items = CartItem.objects.filter(cart = obj)
        available_items = cart_items.filter(item__stock__gte = 1)
        total_discounted_price = 0
        for cart_item in available_items:
            calculated_price = cart_item.item.price * cart_item.quantity
            discounted_price = calculated_price - (calculated_price * (cart_item.item.discount/100))
            total_discounted_price += discounted_price
        return total_discounted_price
    
    # total price of discount
    # calculated with quantity
    def get_total_discount_price(self, obj):
        cart_items = CartItem.objects.filter(cart = obj)
        available_items = cart_items.filter(item__stock__gte = 1)
        total_discount_price = 0
        for cart_item in available_items:
            calculated_price = cart_item.item.price * cart_item.quantity
            discounted_price = (calculated_price * (cart_item.item.discount/100))
            total_discount_price += discounted_price
        return total_discount_price


class TestSerializer(serializers.ModelSerializer):

    class Meta :
        model = Cart
        fields = "__all__"

    def create(self, validated_data):
        try :
            _items = validated_data['items'] if 'items' in validated_data else None
            if not _items:
                raise serializers.ValidationError({"message":"Item List is required."})
            new_cart = super().create(validated_data)
            new_cart.save()

            try :
                for _item in _items:
                    CartItem.objects.create(
                        cart = new_cart,
                        item = _item.item,
                        quantity = _item.quantity
                    )
            except Exception as e:
                raise serializers.ValidationError({"status" : "OOPS! Items Failed", "hint":str(e)})

            return new_cart
        except Exception as e:

            raise serializers.ValidationError({"status" : "OOPS!", "hint":str(e)})