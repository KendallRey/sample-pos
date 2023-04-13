from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from rest_framework import generics
from .models import Account

# @permission_classes([IsAuthenticated])
# @api_view(['GET'])
def get_current_user(request):
    user_details = {}
    response = HttpResponse()
    print("++"+str(request.user))
    try: 
        user_details = {
            "id" : request.user.id,
            "email" : request.user.email,
            "username" : request.user.username,
            "first_name" : request.user.first_name,
            "last_name" : request.user.last_name,
        }
        response.content = user_details
        response.status_code = 201
        return JsonResponse(user_details, safe=False)
    except : 
        response.status_code = 400
        return response

class GetCurrentUser(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Account.objects.all()

    def get(self, request):
        response = HttpResponse()
        try :
            user_details = {
                "id" : request.user.id,
                "email" : request.user.email,
                "username" : request.user.username,
                "first_name" : request.user.first_name,
                "last_name" : request.user.last_name,
            }
            response.content = user_details
            response.status_code = 201
            return response
        except:
            response.status_code = 400
            return response