from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.db.models import Sum
from django.db.models.functions import ExtractMonth

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view

import random
import datetime
import requests
from decimal import Decimal
from distutils.util import strtobool


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
    serializer_class = api_serializer.UserSerializer
    permission_classes = [AllowAny]

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
            return Response({'messages':"password change successfully.",}, status=status.HTTP_201_CREATED) 
        else:
            return Response({"messages": "User Does not exists!"}, status=status.HTTP_404_NOT_FOUND)

class ChangepasswordApiView(generics.CreateAPIView):
    serializer_class = api_serializer.UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        user = User.objects.get(id=user_id)
        if user is not None:
            if check_password(old_password, user.password):
                user.set_password(new_password)
                user.save()
                return Response({"message":"Password changed successfully."})
            else:
                return Response({"message":"Old Password is not correct !."})
                
        else:
            return Response({"message":"Your does not exists"})            
        
    
    
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
        
class StudentNoteApiView(generics.CreateAPIView):
    serializer_class = api_serializer.NoteSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        enrolled_id = self.kwargs['enrolled_id']
        
        user = User.objects.get(id=user_id)
        enrolled = api_models.EnrolledCourse.objects.get(enrolled_id=enrolled_id)
        return api_models.Note.objects.filter(user=user,enrolled=enrolled)
        
        
    
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        enrolled_id = request.data['enrolled_id']
        title = request.data['title']
        note = request.data['note']
        
        user = User.objects.get(id=user_id)
        enrolled = api_models.EnrolledCourse.objects.get(enrolled_id=enrolled_id)
        api_models.Note.objects.create(user=user,course=enrolled.course, note=note, title=title)
        return Response({"message":"Your Note  is saved successfully"}, status=status.HTTP_201_CREATED)
    

class StudentNoteDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = api_serializer.NoteSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        user_id = self.kwargs['user_id']
        enrolled_id = self.kwargs['enrolled_id']
        note_id = self.kwargs['note_id']
        
        user = User.objects.get(id=user_id)
        enrolled = api_models.EnrolledCourse.objects.get(enrolled_id=enrolled_id)
        note_object = api_models.Note.objects.get(user=user, course=enrolled.course,note_id=note_id)
        return note_object

class StudentCourseRatingApiView(generics.CreateAPIView):
    serializer_class = api_serializer.ReviewSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']
        review = request.data['review']
        rating = request.data['rating']
        active = request.data['active']
        user = User.objects.get(id=user_id)
        course = api_models.Course.objects.get(course_id=course_id)

        api_models.Review.objects.create(
            user=user,
            course=course,
            rating = rating,
            review=review,
            active = active
        )
        return Response({"message":"Your review and rating is saved successfully."})

# 538251 enrolled_id
# 029563 note id

class StudentCourseReviewDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = api_serializer.ReviewSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        user_id = self.kwargs['user_id']
        course_id = self.kwargs['course_id']

        user = User.objects.get(id=user_id)
        course = api_models.Course.objects.get(course_id=course_id)
        
        review_object =api_models.Review.objects.get(user=user,course=course)
        return review_object
    


class StudentWhishListApiView(generics.ListCreateAPIView):
    serializer_class = api_serializer.WishlistSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return api_models.Wishlist.objects.filter(user=user)
    
    
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']
        user = User.objects.get(id=user_id)
        course = api_models.Course.objects.get(course_id=course_id)
        
        whish_list = api_models.Wishlist.objects.filter(user=user, course=course).first()
        if whish_list:
            whish_list.delete()
            return Response({"message":"Whish list is deleted"}, status=status.HTTP_201_CREATED)
        else:
            api_models.Wishlist.objects.create(
                user=user,
                course=course   
            )
            return Response({"message":"Wish list is created"}, status=status.HTTP_201_CREATED)
    

class StudentQuestionAnswerListApiView(generics.ListCreateAPIView):
    serializer_class = api_serializer.Question_AnswerSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = api_models.Course.objects.get(course_id=course_id)
        return api_models.Question_Answer.objects.get(course=course)
    
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']
        title = request.data['title']
        message = request.data['message']
        
        user = User.objects.get(id=user_id)
        
        course = api_models.Course.objects.get(course_id=course_id)
        
        question = api_models.Question_Answer.objects.create(
            user=user,
            course=course,
            title=title
        )
        api_models.Question_Answer_Message.objects.create(
            course=course,
            user=user,
            question=question,
            message=message,
        )
        return Response({"message":"Group Conversation is started."}, status=status.HTTP_201_CREATED)
    

class TeacherSummarySerializer(generics.ListAPIView):
    serializer_class = api_serializer.TeacherSummarySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        print(teacher.user.username)
        one_month_ago = datetime.datetime.today() - datetime.timedelta(days=28)
        total_course = api_models.Course.objects.filter(teacher=teacher).count()
        print(total_course)
        
        total_revenue = api_models.CartOrderItem.objects.filter(teacher=teacher,order__payment_status='Paid').aggregate(total_revenue=Sum('price'))['total_revenue'] or 0
        monthly_revenue = api_models.CartOrderItem.objects.filter(teacher=teacher,order__payment_status='Paid', date__gte=one_month_ago).aggregate(total_revenue=Sum('price'))['total_revenue'] or 0
        
        enrolled_course = api_models.EnrolledCourse.objects.filter(teacher=teacher)
        unique_student_ids = set()
        students = []
        for enrolled_user_course in enrolled_course:
            if enrolled_user_course.user_id not in unique_student_ids:
                user = User.objects.get(id=enrolled_user_course.user_id)
                student = {
                    'full_name':user.profile.full_name,
                    'images':user.profile.images.url,
                    'country':user.profile.country,
                    'date':enrolled_user_course.date
                }
                students.append(student)
                unique_student_ids.add(enrolled_user_course.user_id)
        
        return [{
                "total_course": total_course,
                "total_revenue":total_revenue,
                "monthly_revenue":monthly_revenue,
                "total_student":len(students),
            }]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class TeacherCourseListApiView(generics.ListAPIView):
    serializer_class = api_serializer.TeacherSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        teacher_id =self.kwargs['teacher_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        return api_models.Course.objects.filter(teacher=teacher)
    
class TeacherReviewListApiView(generics.ListAPIView):
    serializer_class = api_serializer.TeacherSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        return api_models.Review.objects.filter(course__teacher=teacher)



class TeacherReviewDetailApiView(generics.RetrieveUpdateAPIView):
    serializer_class = api_serializer.ReviewSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        teacher_id = self.kwargs['teacher_id']
        review_id =self.kwargs['review_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        return api_models.Review.objects.get(course__teacher=teacher, id=review_id)
        
        
class TeacherStudentsListApiView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        teacher_id = self.kwargs['teacher_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
    
        enrolled_course = api_models.EnrolledCourse.objects.filter(teacher=teacher)
        unique_student_ids = set()
        students = []
        for course in enrolled_course:
            if course.user_id not in unique_student_ids:
                user = User.objects.get(id=course.user_id)
                student = {
                    'full_name':user.profile.full_name,
                    'images':user.profile.images.url,
                    'country':user.profile.country,
                    'date':course.date
                }
                students.append(student)
                unique_student_ids.add(course.user_id)
        return Response(students)
    

@api_view(["GET"])
def TeacherAllMonthlyEarningApiView(request, teacher_id):
    teacher = api_models.Teacher.objects.get(id=teacher_id)
    monthly_earning_tracker = (
        api_models.CartOrderItem.objects
        .filter(
            teacher=teacher, order__payment_status='Piad')
        .annotate(month=ExtractMonth('date'))
        .values("month")
        .annotate(total_earning=Sum('price'))
        .order_by("month")
    )
    return Response(monthly_earning_tracker)

class TeacherBestSellingCourseApiView(viewsets.ViewSet):
    
    def list(self,request, *args, **kwargs):
        teacher_id = self.kwargs['teacher_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        course_with_total_price = []
        courses = api_models.Course.objects.filter(teacher=teacher)
        for course in courses:
            revenue = course.enrolledcourse_set.aggregate(total_price=Sum('order_item__price'))['total_price'] or 0
            sales = course.enrolledcourse_set.count()
            course_with_total_price.append({
                    "course":course.image.url,
                    "course_title":course.title,
                    "revenue":revenue,
                    "sales":sales
                })
        return Response(course_with_total_price)


class TeacherCourseOrderListApiView(generics.ListAPIView):
    serializer_class = api_serializer.CartOrderItemSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        return api_models.Question_Answer.objects.filter(course__teacher=teacher)
    
class TeacherQuestionAnswerListApiView(generics.ListAPIView):
    serializer_class = api_serializer.Question_AnswerSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        return api_models.Question_Answer.objects.filter(course__teacher=teacher)

class TeacherCouponListCrateApiView(generics.ListCreateAPIView):
    serializer_class = api_serializer.CouponSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        return api_models.Coupon.objects.filter(teacher=teacher)
    
    
class TeacherCouponDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = api_serializer.CouponSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        teacher_id = self.kwargs['teacher_id']
        coupon_id = self.kwargs['coupon_id']
        
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        return api_models.Coupon.objects.get(teacher=teacher,id=coupon_id)
    
class TeacherNotificationListApiView(generics.ListAPIView):
    serializer_class = api_serializer.NotificationSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        return api_models.Notification.objects.filter(teacher=teacher,seen=False)



class TeacherNotificationDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = api_serializer.NotificationSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        teacher_id = self.kwargs['teacher_id']
        notification_id = self.kwargs['noti_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)
        return api_models.Notification.objects.get(teacher=teacher, id=notification_id)

class CourseCreateApiView(generics.CreateAPIView):
    queryset = api_models.Course.objects.all()
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        course_instance = serializer.save()
        variant_data = []
        for key, value in self.request.data.items():
            if key.startswith('variant') and '[variant_title]' in key:
                index = key.split('[')[1].split(']')[0]
                title = index
                
                variant_data = {"title":title}
                item_data_list = []
                current_item = {}
        
        
        
    