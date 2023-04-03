from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Q

from .models import Cart, CartItem
from .serializers import CartSerializer

# Create your views here.

class CartList(generics.ListAPIView):

    serializer_class = CartSerializer
    permission_classes = []

    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        carts = Cart.objects.filter(account = self.request.user)
        return carts

