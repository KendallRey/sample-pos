from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework import generics
from account.AESCipher import AES_Cipher
from account.permissions import IsUserOwner
from rest_framework import generics
from oauth2_provider.views.base import TokenView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
import json
from urllib.parse import urlencode

from account.serializers import AccountUserRegisterSerializer, AccountUserSerializer, ChangePasswordSerializer
from .models import Account
from shop.models import Shop

from oauth2_provider.views.base import TokenView

Cipher = AES_Cipher(
	'qweasdzxcqweasdz',
	'1011121314151617'.encode('utf-8')
	)
class UserRegister(generics.CreateAPIView):
	permission_classes = (AllowAny,)
	serializer_class = AccountUserRegisterSerializer

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
					"id" : str(tempShop.id),
					"name" : tempShop.name,
					"description" : tempShop.description,
				})
			else :
				shop = None
			
			if account.image:
				image_url = account.image.url
			else :
				image_url = None

			user_details = dict({
				"id" : request.user.id,
				"email" : request.user.email,
				"username" : request.user.username,
				"first_name" : request.user.first_name,
				"last_name" : request.user.last_name,
				"image" : image_url,
				"shop" : shop,
			})
			body = json.dumps(user_details)
			encrypted = Cipher.encrypt(body)
			decoded = encrypted.decode("utf-8", "ignore")
			response.content = decoded
			
			response.status_code = 200

			return response
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
	


class AuthLoginView(TokenView):

	@method_decorator(sensitive_post_parameters("password"))
	def post(self, request, *args, **kwargs):

		decrypted = Cipher.decrypt(request.body)
		request._body = decrypted

		url, headers, body, status = self.create_token_response(request)
		if status == 200:
			body = json.loads(body)
			access_token = body.get("access_token")
			if access_token is not None:
				token = get_access_token_model().objects.get(
					token=access_token)
				app_authorized.send(
					sender=self, request=request,
					token=token)
				body = json.dumps(body)
				encrypted = Cipher.encrypt(body)
				decoded = encrypted.decode("utf-8", "ignore")
		response = HttpResponse(content=decoded, status=status)
		# for k, v in headers.items():
		# 	response[k] = v
		return response



class TestApi(generics.GenericAPIView):

	permission_classes = [AllowAny]

	def get(self, request):

		cipher = AES_Cipher(
			'qweasdzxcqweasdz',
			'1011121314151617'.encode('utf-8')
			)
	
		encrypted = cipher.encrypt('Secreat Message to Encrypt')
		encrypted_decoded = encrypted.decode("utf-8", "ignore")
		print('encrypted CBC base64 : ', encrypted_decoded)     

		encrypted_decoded_encoded = encrypted_decoded.encode("utf-8")
		decrypted = cipher.decrypt(encrypted_decoded_encoded)
		print('data: ', decrypted.decode("utf-8", "ignore"))
		response = HttpResponse()
		data = dict(
			value = str(decrypted),
		)
		try :
			return JsonResponse(data=data, safe=False)
		except Exception as e:
			print(str(e))
			response.status_code = 400
			return response
		
	def post(self, request):



		response = HttpResponse()
		try:

			encrypted : str = request.data["value"]
			encoded = encrypted.encode("utf-8")

			decoded = encoded.decode("utf-8", "ignore")
			json_load = json.loads(decoded)

			new_body = dict(
				username = json_load["username"],
				password = json_load["password"],
				grant_type = json_load["grant_type"],
				client_id = json_load["client_id"],
				client_secret = json_load["client_secret"],
			)

			url_encoded = urlencode(new_body)
			bytes_body = bytes(url_encoded, encoding="utf-8")

			return JsonResponse(data=bytes_body, safe=False)
		except:
			response.status_code = 400
			return response
	
