from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Item, ItemCategory
from .serializers import ItemSerializer

# Create your views here.

class ItemList(generics.ListAPIView):

    serializer_class = ItemSerializer
    permission_classes = []

    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Item.objects.all()

class ItemCreate(generics.CreateAPIView):

    serializer_class = ItemSerializer
    permission_classes = []

class ItemUpdate(generics.UpdateAPIView):

    serializer_class = ItemSerializer
    permission_classes = []
    lookup_field = 'id'

    queryset = Item.objects.all()
