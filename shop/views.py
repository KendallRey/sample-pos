from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Shop, ShopCategory
from .serializers import ShopSerializer, ShopCategorySerializer
from .permissions import IsSuperUser

# Create your views here.

class ShopCategoryList(generics.ListAPIView):
    """
    `GET` for list,
    Return categories
    """
    serializer_class = ShopCategorySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        # try:
        #     shop = Shop.objects.get(account=self.request.user)
        # except :
        #     return []
        # if shop is None:
        #     return []
        # query_set = ShopCategory.objects.filter(shop=shop)

        # return query_set
        return ShopCategory.objects.all()
class ShopCategoryCreate(generics.CreateAPIView):
    """
    `GET` for list,
    Return categories of their own shop, empty if user doesn't have a shop
    """
    serializer_class = ShopCategorySerializer
    permission_classes = [IsSuperUser]

class ShopCategoryRetrieve(generics.RetrieveAPIView):
    """
    `retrieve/<str:id>` for retrieving order item,
    """
    serializer_class = ShopCategorySerializer
    permission_classes = []
    lookup_field = 'id'

    queryset = ShopCategory.objects.all()

class ShopCategoryUpdate(generics.RetrieveUpdateAPIView):
    """
    `update/<str:id>` for retrieving order item,
    """
    serializer_class = ShopCategorySerializer
    permission_classes = [IsSuperUser]
    lookup_field = 'id'

    queryset = ShopCategory.objects.all()

class ShopList(generics.ListAPIView):

    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Shop.objects.all()

class ShopCreate(generics.CreateAPIView):

    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]

class ShopRetrieve(generics.GenericAPIView):

    # serializer_class = ShopSerializer
    # permission_classes = []

    queryset = Shop.objects.all()
    
    def get(self,request):
        try:
            shop = Shop.objects.filter(account = self.request.user)
            if shop.count() <= 1:
                serializer = ShopSerializer(shop, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response({"errors" : ["User doesn't have a shop!"]}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"errors" : ["OOPS! something went wrong"]}, status=status.HTTP_404_NOT_FOUND)
        

class ShopUpdate(generics.UpdateAPIView):

    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    queryset = Shop.objects.all()

class ShopDelete(generics.DestroyAPIView):

    serializer_class = ShopSerializer
    permission_classes = []
    lookup_field = 'id'

