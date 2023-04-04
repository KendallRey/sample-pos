from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Q

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

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


