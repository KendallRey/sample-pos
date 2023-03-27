from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from shop.models import Shop
from .models import Item, ItemCategory
from .serializers import ItemSerializer, ItemCategorySerializer

# Create your views here.

class ItemCategoryList(generics.ListAPIView):
    """
    `GET` for list,
    Return categories of their own shop, empty if user doesn't have a shop
    """
    serializer_class = ItemCategorySerializer
    permission_classes = []

    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        shop = Shop.objects.get(account=self.request.user)
        if shop is None:
            return []
        query_set = ItemCategory.objects.filter(shop=shop)

        return query_set

class ItemList(generics.ListAPIView):

    serializer_class = ItemSerializer
    permission_classes = []

    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Item.objects.all()

class ItemCreate(generics.CreateAPIView):

    serializer_class = ItemSerializer
    permission_classes = []

class ItemRetrieve(generics.RetrieveAPIView):

    serializer_class = ItemSerializer
    permission_classes = []
    lookup_field = 'id'

    queryset = Item.objects.all()

class ItemUpdate(generics.UpdateAPIView):

    serializer_class = ItemSerializer
    permission_classes = []
    lookup_field = 'id'

    queryset = Item.objects.all()

class ItemDelete(generics.DestroyAPIView):

    serializer_class = ItemSerializer
    permission_classes = []
    lookup_field = 'id'
