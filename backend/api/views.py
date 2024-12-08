from django.shortcuts import render
from api import serializers as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


import random

from account.models import User


def generate_random_opt_code(length=6):
    otp = ''.join([str(random.randint(0,9)) for _ in range(length)])
    return otp

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer
    
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = api_serializer.RegisterSerializer
    permission_classes = [AllowAny]
    


class PasswordRegisterEmailVerifyApiView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer
    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.filter(email=email).first()
        if user:
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            user.refresh_token = refresh_token
            user.otp =generate_random_opt_code()
            user.save()
            link = f'http://localhost:5173/crate-new-password/?opt{user.otp}&uuidb64={uuidb64}&=refresh_token{refresh_token}'
        
            print(link)
        return user

class PasswordChangeApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer
    
    def create(self, request, *args, **kwargs):
        otp = request.data['otp']
        uuidb64 = request.data['uuidb64']
        password = request.data['password']
        user = User.objects.get(id=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            user.opt = ''
            user.save()
            return Response({'messages':"password change successfully.",}, status=status.HTTP_201_CREATED) 
        else:
            return Response({"messages":"User Does not exists!"}, status=status.HTTP_404_NOT_FOUND)