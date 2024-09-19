from django.shortcuts import render
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

import random
import requests
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


class CheckOutApiView(generics.RetrieveAPIView):
    serializer_class = api_serializer.CartOrderSerializer
    permission_classes = [AllowAny]
    lookup_field = 'oid'
    queryset = api_models.CartOrder.objects.all()
   
   

class CouponApiView(generics.CreateAPIView):
    serializer_class = api_serializer.CouponSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        order_oid = request.data['order_oid']
        coupon_code = request.data['coupon_code']
        order = api_models.CartOrder.objects.get(oid=order_oid)
        coupon = api_models.Coupon.objects.get(code=coupon_code)
        if coupon:
            order_items = api_models.CartOrder.objects.filter(order=order, teacher=coupon.teacher)
            for i in order_items:
                if not coupon in order.coupons:
                    discount = i.total * coupon.discount
                    i.total = discount
                    i.price= discount
                    i.saved = discount
                    i.applied_coupon = True
                    i.coupons.add(coupon)
                    order.coupons.add(coupon)
                    order.total -= discount
                    order.sub_total -= discount
                    order.saved += discount
                    i.save()
                    order.save()
                    coupon.used_by.add(order.student)
                    
                    return Response({"message":"Coupon Found and Activated ."}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':'Coupon Already Applied .',},status=status.HTTP_200_OK)
        else:
            raise Response({"message":"Coupon Not Found."}, status=status.HTTP_404_NOT_FOUND) ()
       


def get_access_token(clint_id,secret_key):
    token_url = 'https://api.sandbox.paypal.con/v1/oauth/token'
    data = {'grant_type':'clint_credentials'}
    auth = (clint_id, secret_key)
    response = requests.get(token_url,data=data, auth=auth)
    if response.status_code == 200:
        print('Access Token =====>', response.json()['access_token'])
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token form paypal {response.status_code}")
    
# PAYPAL_CLIENT_ID = settings.PAYPAL_CLIENT_ID  # this come from .env
# PAYPAL_SECRET_ID = settings.PAYPAL_SECRET_ID # this come from .env

class PaymentSuccessApiView(generics.CreateAPIView):
    serializer = api_serializer.CartOrderSerializer
    def get_queryset(self):
        return api_models.CartOrder.objects.all()
    
    def create(self, request, *args, **kwargs):
        order_id = request.data['order_id']
        paypal_order_id = request.data['paypal_order_id']
    
        order = api_models.CartOrder.objects.get(id=order_id)
        order_items = api_models.CartOrderItem.objects.filter(order=order) 
        
        # paypal payment success
        if paypal_order_id != 'null':
            paypal_api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order_id}"
            headers = {
                "Content-Type":'application/json',
                # "Authorization":f"Bearer {get_access_token(PAYPAL_CLIENT_ID,PAYPAL_SECRET_ID)}"
            }
            response = requests.get(paypal_api_url, headers=headers)
            if response.status_code == 200:
                paypal_order_data = response.data
                paypal_payment_status = paypal_order_data['status']
                if paypal_payment_status == 'COMPLETED':
                    if order.payment_status == 'Processing':
                        order.payment_status  == "Paid"
                        order.save()
                        api_models.Notification.objects.create(user=order.student,order=order,type='Course Enrollment Completed')
                        for o in order_items:
                            api_models.Notification.objects.create(
                                teacher= o.teacher,
                                order = order,
                                order_items = o,
                                type = 'New Order'
                            )
                            api_models.EnrolledCourse.objects.create(
                                course = o.course,
                                user = order.student,
                                teacher = o.teacher,
                                order_items = o
                                
                    
                            )
                    else:
                        return Response({"message":"You have already paid. Thanks you"})
                else:
                    return Response({"message":"Payment is not successfully."})
            return Response({"message":"An API error is Occured from paypal."})
        

class SearchCourseApiView(generics.ListAPIView):
    serializer_class = api_serializer.CounterSerializer
    parser_classes = [AllowAny]

    
    def get_queryset(self):
        query =  self.request.GET.get('query')
        return api_models.Course.objects.filter(title__icontains=query, teacher_course_start='Published', platform_status='Published')
    

class StudentSummaryApiView(generics.ListAPIView):
    serializer_class = api_serializer.StudentSummarySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        total_courser = api_models.EnrolledCourse.objects.filter(user=user).count()
        completed_lesson = api_models.CompletedLesson.objects.filter(user=user).count()
        achieved_certificates = api_models.Certificate.objects.filter(user=user).count()
    
        return [{'total_course':total_courser,"completed_lessons":completed_lesson,"achieved_certificates":achieved_certificates}]
                            
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudentCourseListApiView(generics.ListAPIView):
    serializer_class = api_serializer.EnrolledCourseSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return api_models.EnrolledCourse.objects.filter(user=user)
    

class StudentCourseDetailApiView(generics.RetrieveAPIView):
    serializer_class = api_serializer.EnrolledCourseSerializer
    permission_classes = [AllowAny]
    lookup_field = 'enrolled_id'
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        enrolled_id = self.kwargs['enrolled_id']
        user = User.objects.get(id=user_id)
        return api_models.EnrolledCourse.objects.get(user=user, enrolled_id=enrolled_id)
    
class StudentCourseCompletedApiView(generics.CreateAPIView):
    serializer_class = api_serializer.CompletedLessonSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']
        variant_item_id = request.data['variant_item_id']

        user = User.objects.get(id=user_id)
        course = api_models.Course.objects.get(id=course_id)
        variant_item = api_models.VariantItem.objects.get(variant_item_id=variant_item_id)
        completed_lesson = api_models.CompletedLesson.objects.filter(user=user, course=course,variant_item=variant_item).first()
        if completed_lesson:
            completed_lesson.delete()
            return Response({'message':"Course marked as not completed"})
        else:
            api_models.CompletedLesson.objects.create(user=user, course=course,variant_item=variant_item)
            return Response({'message':"Course marked as completed"})