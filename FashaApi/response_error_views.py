from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse

def not_authenticated(request,format='json'):
    return JsonResponse({'error': 'not_authenticated'}, status=HTTP_401_UNAUTHORIZED)

def bad_request(request,format='json'):
    return JsonResponse({'error': 'not_authenticated'}, status=HTTP_400_BAD_REQUEST)
