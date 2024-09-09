from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from account.models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import models as serializer_model


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'images', 'country', 'full_name', 'bio', 'date']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "password fields do not match!"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )
        email_user, _ = user.email.split("@")
        user.username = email_user
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLogin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    course_count = None

    class Meta:
        model = serializer_model.Category
        fields = ['title', 'image', 'slug', 'course_count']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['user', 'image', 'full_name', 'bio', 'job_description', 'facebook', 'twitter', 'linkedin', 'counter']
        model = serializer_model.Teacher



class VariantItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = serializer_model.VariantItem

class VariantSerializer(serializers.ModelSerializer):
    variant_items = VariantItemSerializer()
    class Meta:
        fields = ['course','title','variant_id','date', 'variant_items']
 
        model = serializer_model.Variant

class CompletedLessonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = serializer_model.CompletedLesson


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = serializer_model.Note
        

class Question_AnswerSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = serializer_model.Question_Answer

class ReviewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    class Meta:
        fields = '__all__'
        model = serializer_model.Review



class EnrolledCourseSerializer(serializers.ModelSerializer):
    lectures = VariantItemSerializer(many=True, read_only=True)
    completed_lesson = CompletedLessonSerializer(many=True, read_only=True)
    curriculum = VariantSerializer(many=True, read_only=True)
    note = NoteSerializer(many=True, read_only=True)
    question_answer = Question_AnswerSerializer(many=True, read_only=True)
    review = ReviewSerializer(many=True, read_only=True)
    class Meta:
        fields = '__all__'
        model = serializer_model.EnrolledCourse

class CourseSerializer(serializers.ModelSerializer):
    students = EnrolledCourseSerializer(many=True)
    curriculum = VariantSerializer(many=True)
    lectures = VariantSerializer(many=True)
    class Meta:
        model = serializer_model.Course
        fields = ['title','description','price','category','teacher','image','file','language','level','teacher_course_start','course_id','slug','date', 'students','curriculum','lectures','average_rating','rating_count','reviews']

class Question_Answer_MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = serializer_model.Question_Answer_Message
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = serializer_model.Cart
        fields = '__all__'

class CartOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = serializer_model.CartOrderItem
        fields = '__all__'

class CartOrderSerializer(serializers.ModelSerializer):
    order_items = CartOrderItemSerializer()
    class Meta:
        model = serializer_model.CartOrder
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = serializer_model.Certificate
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = serializer_model.Notification


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = serializer_model.Coupon


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = serializer_model.Wishlist
        fields = '__all__'


class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = serializer_model.Counter
        fields = '__all__'
