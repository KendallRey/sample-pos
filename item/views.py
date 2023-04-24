from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shop.models import Shop
from .models import Item, ItemCategory, ItemImage
from .serializers import ItemSerializer, ItemCategorySerializer, ItemImageSerializer

# Create your views here.

class ItemCategoryList(generics.ListAPIView):
	"""
	`GET` for list,
	Return categories of their own shop, empty if user doesn't have a shop
	"""
	serializer_class = ItemCategorySerializer
	permission_classes = [IsAuthenticated]

	filter_backends = [DjangoFilterBackend]

	def get_queryset(self):
		shop = Shop.objects.get(account=self.request.user)
		if shop is None:
			return []
		query_set = ItemCategory.objects.filter(shop=shop)

		return query_set

class ItemList(generics.ListAPIView):

	serializer_class = ItemSerializer
	permission_classes = [IsAuthenticated]

	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = {
		'created_at' : ['gte','lte'],
		'name' : ['contains'],
		'price' : ['gte','lte'],
		'categories__id' : ['exact'],
		}
	ordering_fields = [
		'created_at',
		'price',
		]

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

class ItemUpdate(generics.RetrieveUpdateAPIView):

	serializer_class = ItemSerializer
	permission_classes = []
	lookup_field = 'id'

	queryset = Item.objects.all()

class ItemDelete(generics.DestroyAPIView):

	serializer_class = ItemSerializer
	permission_classes = []
	lookup_field = 'id'

class ItemImageList(generics.ListAPIView):

	serializer_class = ItemImageSerializer
	permission_classes = []
	queryset = ItemImage.objects.all()

class ItemImageCreate(APIView):

	def post(self, request):
		serializer = ItemImageSerializer(data=request.data)
		try:
			if serializer.is_valid():
				item = Item.objects.get(id = serializer.validated_data['item'].id)
				if item.shop is None:
					return Response({"errors" : ["Invalid item!"]}, status=status.HTTP_404_NOT_FOUND)
				if item.shop.account.id is not request.user.id:
					return Response({"errors" : ["Item not yours!"]}, status=status.HTTP_404_NOT_FOUND)

				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
		except:
			return Response({"errors" : ["OOPS! something went wrong"]}, status=status.HTTP_404_NOT_FOUND)

class ItemImageUpdate(APIView):

	def put(self, request, id):
		try:
			image = ItemImage.objects.get(id = id)
			if image.item.shop is None:
				return Response({"errors" : ["Invalid item!"]}, status=status.HTTP_404_NOT_FOUND)
			if image.item.shop.account.id is not request.user.id:
				return Response({"errors" : ["Item not yours!"]}, status=status.HTTP_404_NOT_FOUND)
			
			serializer = ItemImageSerializer(image, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
		except:
			return Response({"errors" : ["OOPS! something went wrong"]}, status=status.HTTP_404_NOT_FOUND)
