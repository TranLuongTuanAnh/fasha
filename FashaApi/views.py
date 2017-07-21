from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth.models import User
from FashaApi.models import UserSerializer
from models import PosterSerializer
from pprint import pprint
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authentication import TokenAuthentication
from fasha.backends import AuthByMail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# @login_required()
def index(request):
    print "base dir path", BASE_DIR
    return JsonResponse({"success":"1"})

@api_view(['POST'])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(email=email,password=password)
    if not user:
        return JsonResponse({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse({"token":token.key})

# Create your views here.
class UserRegister(APIView):
    """
    Creates the user
    """
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        # pprint(serializer)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return JsonResponse(json,status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Poster(LoginRequiredMixin, APIView):
    def post(self,request,format='json'):
        request.data['owner_id'] = request.user.username
        serializer = PosterSerializer(data=request.data)
        if serializer.is_valid():
            poster = serializer.create(serializer.validated_data)
            json = serializer.data
            return JsonResponse(json,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
