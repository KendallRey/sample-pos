from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Q
from rest_framework.generics import GenericAPIView

from account.models import Account
from item.models import Item
from .models import Cart, CartItem
from rest_framework.views import APIView
from .serializers import CartSerializer, CartItemSerializer, TestSerializer

# Create your views here.

class CartList(generics.ListAPIView):

    serializer_class = CartSerializer
    permission_classes = []

    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        carts = Cart.objects.filter(account = self.request.user)
        return carts

class CartItemList(generics.ListAPIView):

    serializer_class = CartItemSerializer
    permission_classes = []

    filter_backends = [DjangoFilterBackend]

    lookup_field = "id"

    def get_queryset(self):
        cart_id = self.kwargs.get('id')
        cart_items = CartItem.objects.filter(cart__id = cart_id)
        # return carts
        return cart_items

class TestBulkCreate(APIView):

    serializer_class = TestSerializer
    permission_classes = []

    filter_backends = [DjangoFilterBackend]

    lookup_field = "id"

    def get_queryset(self):
        cart_id = self.kwargs.get('id')
        cart_items = CartItem.objects.filter(cart__id = cart_id)
        # return carts
        return cart_items

    def post(self, request):
        try :
            _items = request.data['items']
            if not _items:
                return Response({"errors" : ["Invalid items!"]}, status=status.HTTP_404_NOT_FOUND)
            if not _items:
                return Response({"errors" : ["Invalid items!"]}, status=status.HTTP_404_NOT_FOUND)
            
            cart = Cart.objects.create(account = request.user)
            cart.save()

            try :
                for _item in _items:
                    item = Item.objects.get(pk = _item["id"])
                    CartItem.objects.create(
                        cart = cart,
                        item = item,
                        quantity = _item["quantity"]
                    )
            except Exception as e:
                cart.delete()
                return Response({"errors" : ["Invalid items2!"],"hint":str(e)}, status=status.HTTP_404_NOT_FOUND)
            new_cart = {
                "id" : cart.id
            }
            return JsonResponse(new_cart, safe=False)
        except Exception as e:
            cart.delete()
            return Response({"errors" : ["Idawdaw!"],"hint":str(e)}, status=status.HTTP_404_NOT_FOUND)

