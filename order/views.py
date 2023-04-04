from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import OrderItemSerializer
from .models import OrderItem

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
