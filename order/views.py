from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import F
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from django.core import serializers
from item.models import Item

from django.db import models, transaction

from .serializers import OrderItemSerializer, RatingSerializer
from .models import OrderItem, Rating

from cart.models import CartItem
from shop.models import Shop

# Create your views here.
class OrderItemList(generics.ListAPIView):

    """
    `list` for ALL order items in of user,
    `list/<shop:id>` for order items of user in the shop,
    """

    serializer_class = OrderItemSerializer
    permission_classes = []

    def get_queryset(self):
        try :
            shop_id = self.kwargs.get('id')
            shop = Shop.objects.get(account = self.request.user)
            query_set = OrderItem.objects.filter(shop__account = self.request.user)
            if shop_id is not None:
                return query_set.filter(shop = shop)
            return query_set
        except :
            return Response({"errors" : ["User doesn't have a shop!"]}, status=status.HTTP_404_NOT_FOUND)

class OrderItemCreate(generics.CreateAPIView):
    """
    `create` for creating order item,
    auto select shop of selected cart_item,
    """

    serializer_class = OrderItemSerializer
    permission_classes = []

    # def create(self, request, *args, **kwargs):
    #     print("id::"+request.data['cart_item'])
    #     try :
    #         print("id::"+request.data['cart_item'])
    #     except:
    #         return Response({"errors" : ["User doesn't have a shop!"]}, status=status.HTTP_404_NOT_FOUND)
    # return super().create(request, *args, **kwargs)

class OrderItemRetrieve(generics.RetrieveAPIView):
    """
    `retrieve/<str:id>` for retrieving order item,
    """
    serializer_class = OrderItemSerializer
    permission_classes = []

    lookup_field = 'id'

    queryset = OrderItem.objects.all()

class OrderItemUpdate(generics.UpdateAPIView):
    """
    `update/<str:id>` for updating order item,
    """
    serializer_class = OrderItemSerializer
    permission_classes = []

    lookup_field = 'id'

    queryset = OrderItem.objects.all()

class OrderItemDelete(generics.RetrieveDestroyAPIView):
    """
    `delete/<str:id>` for deleting order item,
    """
    serializer_class = OrderItemSerializer
    permission_classes = []

    lookup_field = 'id'

    queryset = OrderItem.objects.all()


# Change Status to ORDERED
# Change Item stock to current value minus cart item quantity
class OrderItemAccept(APIView):
    """
    `accept/<str:id>` for accepting order item,
    """
    permission_classes = []
    # serializer_class = OrderItemSerializer

    # The explicit transaction.commit() and transaction.rollback()
    # are not strictly necessary here, as transactions are
    # automatically committed or rolled back when the block exits.

    def post(self, request, id):
        try:
            with transaction.atomic():
                order_item = OrderItem.objects.select_for_update().get(id=id)  # Lock the row for update
                if order_item.status == "ORDERED":
                    return Response({"errors": ["Item already ordered!"]}, status=status.HTTP_404_NOT_FOUND)

                item_stock = Item.objects.select_for_update().get(id=order_item.cart_item.item.id)
                if item_stock.stock < order_item.cart_item.quantity:
                    return Response({"errors": ["Not enough stock!"]}, status=status.HTTP_404_NOT_FOUND)

                order_item.status = "ORDERED"
                order_item.save()

                item_stock.stock -= order_item.cart_item.quantity
                item_stock.save()

            return Response(data=OrderItemSerializer(order_item).data, status=status.HTTP_200_OK)

        except OrderItem.DoesNotExist:
            return Response({"errors": ["Order Item not found!"]}, status=status.HTTP_404_NOT_FOUND)
        except Item.DoesNotExist:
            return Response({"errors": ["Item not found!"]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('%s' % type(e))
            return Response({"errors": ["OOPS! Something went wrong"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class OrderItemAccept(generics.CreateAPIView):
#     """
#     `accept/<str:id>` for accepting order item,
#     """

#     serializer_class = OrderItemSerializer
#     permission_classes = []

#     lookup_field = 'id'

#     queryset = OrderItem.objects.all()

    # def create(self, request, *args, **kwargs):
    #     item_stock = Item.objects.get(id=self.cart_item.item.id).stock
    #     if item_stock < self.cart_item.quantity:
    #         return Response({"errors" : ["Not enough stock!"]}, status=status.HTTP_404_NOT_FOUND)
    #     try :
    #         Item.objects.filter(id=self.cart_item.item.id).update(stock = F('stock')+(-self.cart_item.quantity))
    #         return Response({"errors" : ["User doesn't have a shop!"]}, status=status.HTTP_200_OK)
    #     except :
    #         return Response({"errors" : ["User doesn't have a shop!"]}, status=status.HTTP_404_NOT_FOUND)

    # def cr(self):
    #     try :
    #         Item.objects.filter(id=self.cart_item.item.id).update(stock = F('stock')+(-self.cart_item.quantity))
    #         return Response({"errors" : ["User doesn't have a shop!"]}, status=status.HTTP_200_OK)
    #     except :
    #         return Response({"errors" : ["User doesn't have a shop!"]}, status=status.HTTP_404_NOT_FOUND)
    #     return super().get_object()
    
    # serializer_class = OrderItemSerializer
    # permission_classes = []


class RatingList(generics.ListAPIView):
    """
    `create` for creating,
    """
    serializer_class = RatingSerializer
    permission_classes = []

    queryset = Rating.objects.all()

class RatingCreate(generics.CreateAPIView):
    """
    `create` for creating,
    """
    serializer_class = RatingSerializer
    permission_classes = []

class RatingUpdate(generics.UpdateAPIView):
    """
    `update/<str:id>` for creating,
    """
    serializer_class = RatingSerializer
    permission_classes = []
