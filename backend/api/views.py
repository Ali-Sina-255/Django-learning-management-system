from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

import random
from decimal import Decimal
from api import serializers as api_serializer
from api import models as api_models

from account.models import User


def generate_random_opt_code(length=6):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
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
            user.otp = generate_random_opt_code()
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
            return Response({'message': "password change successfully.", }, status=status.HTTP_201_CREATED)

        else:
            return Response({"messages": "User Does not exists!"}, status=status.HTTP_404_NOT_FOUND)


class CategoryListAPIView(generics.ListAPIView):
    queryset = api_models.Category.objects.filter(active=True)
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]


class CourseListAPIView(generics.ListAPIView):
    queryset = api_models.Course.objects.filter(teacher_course_start='Published', platform_status='Published')
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]


class CourseDetailApiView(generics.RetrieveAPIView):
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        return api_models.Course.objects.get(slug=slug, teacher_course_start='Published', platform_status='Published')


class CartAPIView(generics.CreateAPIView):
    queryset = api_models.Cart.objects.all()
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        course_id = request.data['course_id']
        user_id = request.data['user_id']
        price = request.data['price']
        country_name = request.data['country_name']
        cart_id = request.data['cart_id']

        course = api_models.Course.objects.filter(id=course_id).first()

        if user_id != 'undefined':
            user = User.objects.filter(id=user_id).first()
        else:
            user = None
        try:
            country_object = api_models.Counter.objects.filter(name=country_name).first()
            country = country_object.name

        except:
            country_object = None
            country = "Afghanistan"

        if country_object:
            tax_rate = country_object.tax_rate / 100
        else:
            tax_rate = 0

        cart = api_models.Cart.objects.filter(cart_id=cart_id, course=course).first()
        if cart:
            cart.course = course
            cart.user = cart
            cart.price = price
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price)
            cart.save()

            return Response({"message": "Cart Update successfully"}, status=status.HTTP_200_OK)

        else:
            cart = api_models.Cart()
            cart.user = cart
            cart.price = price
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price)
            cart.save()

            return Response({"message": "Cart added successfully"}, status=status.HTTP_201_CREATED)


class CartListApiView(generics.ListAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        return api_models.Cart.objects.get(cart_id=cart_id)


class CartItemDeleteApiView(generics.DestroyAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        cart_id = self.kwargs['cart_id']
        item_id = self.kwargs['item_id']
        return api_models.Cart.objects.filter(cart_id=cart_id, id=item_id).first()


class CartStatsApiView(generics.RetrieveAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes =[AllowAny]
    lookup_field = 'cart_id'
    
    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        return api_models.Cart.objects.filter(cart_id=cart_id)
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        total_price = 0.00
        total_tax = 0.00
        total_total = 0.00
        
        for cart_item in queryset:
            total_price += float(self.calculate_price(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_total += round(float(self.calculate_total(cart_item)),2)
        
        data = {
            'price':total_price,
            "tax":total_tax,
            "total":total_total
        }
        return Response(data)
            
    def calculate_price(self, cart_item):
        return cart_item.price
    
    def calculate_tax(self, cart_item):
        return cart_item.price
    
    def calculate_total(self, cart_item):
        return cart_item.price
    
    

class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.CartOrderSerializer
    permission_classes = [AllowAny]
    queryset = api_models.CartOrder.objects.all()
    
    
    def create(self, request, *args, **kwargs):
        full_name = request.data['full_name']
        email = request.data['email']
        country = request.data['country']
        cart_id = request.data['cart_id']
        user_id = request.data['user_id']
        
        if user_id !=0:
            user = User.objects.get(id=user_id)
        else:
            user = None
            
        cart_items = api_models.Cart.objects.filter(cart_id=cart_id)
        total_price = Decimal(0.00)
        total_tax = Decimal(0.00)
        total_initial_total = Decimal(0.00)
        total_total = Decimal(0.00)
        order = api_models.CartOrder.objects.create(
            full_name=full_name,
            email=email,
            country=country,
            student=user
            )
        
        for card in cart_items:
            api_models.CartOrderItem.objects.create(
                order=order,
                course=card.course,
                price = card.price,
                total = card.total,
                initial_total = card.initial_total,
                teacher = card.course.teacher    
            )
            total_price += Decimal(card.price)
            total_initial_total += Decimal(card.total)
            total_total += Decimal(card.total)
            
            order.teachers.add(card.course.teacher)
        order.sub_total = total_price
        order.initial_total = total_initial_total
        order.total = total_total
        order.save()
        return Response({"message":"Your order is created successfully."}, status=status.HTTP_201_CREATED)