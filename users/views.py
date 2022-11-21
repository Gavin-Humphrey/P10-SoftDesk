from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serilizers import UserSerializer, SignupSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics



#Class based view to register user
class SignupUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = SignupSerializer

# Create your views here.
