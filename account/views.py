from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from django.core import serializers
from rest_framework import generics
from account.permissions import IsUserOwner

from account.serializers import AccountUserSerializer, ChangePasswordSerializer
from .models import Account
from shop.models import Shop
from shop.serializers import ShopSerializer

# @permission_classes([IsAuthenticated])
# @api_view(['GET'])
# def get_current_user(request):
#     user_details = {}
#     response = HttpResponse()
#     print("++"+str(request.user))
#     try: 
#         user_details = {
#             "id" : request.user.id,
#             "email" : request.user.email,
#             "username" : request.user.username,
#             "first_name" : request.user.first_name,
#             "last_name" : request.user.last_name,
#         }
#         response.content = user_details
#         response.status_code = 201
#         return JsonResponse(user_details, safe=False)
#     except : 
#         response.status_code = 400
#         return response

class GetCurrentUser(generics.GenericAPIView):

	permission_classes = [IsAuthenticated]
	queryset = Account.objects.all()

	def get(self, request):
		response = HttpResponse()
		try :
			account = Account.objects.get(id = request.user.id)
			shopList = Shop.objects.filter(account=request.user)
			if shopList.count() >= 1 :
				tempShop = shopList.first()
				shop = dict({
					"id" : tempShop.id,
					"name" : tempShop.name,
					"description" : tempShop.description,
				})
			else :
				shop = None
			
			if account.image:
				image_url = account.image.url
			else :
				image_url = None

			user_details = {
				"id" : request.user.id,
				"email" : request.user.email,
				"username" : request.user.username,
				"first_name" : request.user.first_name,
				"last_name" : request.user.last_name,
				"image" : image_url,
				"shop" : shop,
			}

			response.content = user_details
			response.status_code = 201
			return JsonResponse(user_details, safe=False)
		except Exception as e:
			print(str(e))
			response.status_code = 400
			return response

class UpdateUser(generics.UpdateAPIView):
	"""
	`update/<str:id>` for creating,
	"""
	serializer_class = AccountUserSerializer
	permission_classes = [IsUserOwner]

	lookup_field = "id"

	def get_queryset(self):
		return Account.objects.all()
	

class UpdateUserPassword(generics.UpdateAPIView):
	"""
	`update/<str:id>` for creating,
	"""
	serializer_class = ChangePasswordSerializer
	permission_classes = [IsUserOwner]

	lookup_field = "id"

	def get_queryset(self):
		return Account.objects.all()
	
