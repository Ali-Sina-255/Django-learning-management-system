from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from account.models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','full_name','email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','images','country','full_name','bio','date']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True) 
    class Meta:
        model = User
        fields = ['full_name','email','password','password2']
        
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':"password fields do not match!"})
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            full_name =validated_data['full_name'],
            email =validated_data['email'],
        )
        email_user, _ = user.email.split("@")
        user.username = email_user
        user.set_password(validated_data['password'])
        user.save()
        return user