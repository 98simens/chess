from main.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token

class LoginEndpoint(APIView):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if(user is not None):
            token = Token.objects.get(user=user)
            return JsonResponse(data={"message": "Login Success", "token": token.key, "username": user.username}, status=200)
        else:
            return JsonResponse(data={"error": "Login Failed"}, status=403)

class RegisterEndpoint(APIView):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')


        user = User.objects.create_user(email=None, username=username, password=password)
        if(user is not None):
            token = Token.objects.create(user=user)
            return JsonResponse(data={"message": "Register Success", "token": token.key, "username": user.username}, status=200)
        else:
            return JsonResponse(data={"error": "Register Failed"}, status=403)

