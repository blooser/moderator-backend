from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(["POST"])
def login(request):
    data = request.data
 
    username = data['username']
    password = data['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        return Response({
            "username": username,
            "password": password
        })

    return Response({
        "User not authenticated": "You are not allowed enter the page"
    }, status=status.HTTP_401_UNAUTHORIZED)

