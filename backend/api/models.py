from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from account.models import Profile, User
from shortuuid.django_fields import ShortUUIDField
from moviepy.editor import VideoFileClip
import math


LANGUAGE_CHOICES = (
    ('English', 'English'),
    ('Dari', 'Dari'),
    ('Pashto', 'Pashto'),
    ('Chinese', 'Chinese'),
    ('Arabic', 'Arabic'),
)

LEVEL_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
)

TEACHER_COURSE_START_CHOICES = (
    ('Published', 'Published'),
    ('Disabled', 'Disabled'),
    ('Draft', 'Draft'),
)
PLATFORM_STATUS_CHOICES = (
    ('Published', 'Published'),
    ('Pending', 'Pending'),
    ('Draft', 'Draft'),
)
RATING_STATUS = (
    (1, "1 Star"),
    (2, "2 Star"),
    (3, "3 Star"),
    (4, "4 Star"),
    (5, "5 Star"),
)

NOTE_TYPE_CHOICES = (
    ("New Order","New Order"),
    ("New Review","New Review"),
    ("New Course Question","New Course Question"),
    ("Draft","Draft"),
)

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='teachers')
    image = models.FileField(upload_to='course-file', blank=True, null=True, default='course.jpg')
    full_name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    counter = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.full_name

class Category(models.Model):
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    image = models.FileField(upload_to='course-file/category/')
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def course_count(self):
        return Course.objects.filter(category=self).count()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    image = models.FileField(upload_to='course-file/course', blank=True, null=True)
    file = models.FileField(upload_to='course-file/course', blank=True, null=True)
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, default='English')
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES, default='Beginner')
    teacher_course_start = models.CharField(max_length=255, choices=TEACHER_COURSE_START_CHOICES)
    platform_status = models.CharField(max_length=255, choices=PLATFORM_STATUS_CHOICES)
    course_id = ShortUUIDField(unique=True, max_length=30, length=6, alphabet='1234567890')
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course,self).save(*args, **kwargs)
    
    def lectures(self):
        return VariantItem.objects.filter(variant__course=self)
    
    def students(self):
        return EnrolledCourse.objects.filter(course=self)

    def curriculum(self):
        return VariantItem.objects.filter(variant__course=self)

    def average_rating(self):
        average_rating = Review.objects.filter(course=self, active=True).aggregate(avg_rating=models.Avg('rating'))
        return average_rating['avg_rating']

    def rating_count(self):
        return Review.objects.filter(course=self, active=True).count()

    def reviews(self):
        return Review.objects.filter(course=self, active=True)
    
class Variant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    variant_id = ShortUUIDField(unique=True, length=6, alphabet='1234567890')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title

    def variant_items(self):
        return VariantItem.objects.filter(variant=self)

class VariantItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variant_items')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='course-file')
    variant_item_id = ShortUUIDField(unique=True, length=6, max_length=30, alphabet='1234567890')
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.variant.title} - {self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file:
            clip = VideoFileClip(self.file.path)
            duration_seconds = clip.duration
            minutes, remainder = divmod(duration_seconds, 60)
            minutes = math.floor(minutes)
            seconds = math.floor(remainder)
            duration_text = f"{minutes}m {seconds}s"  # e.g., 60m 30s
            self.content_duration = duration_text
            super().save(update_fields=['content_duration'])

class Question_Answer(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    question_a_id = ShortUUIDField(unique=True, length=6, max_length=30, alphabet='1234567890')
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f'{self.user.username} - {self.course.title}'

    class Meta:
       ordering = ['-date']
    
    def profile(self):
        return Profile.objects.get(user=self.user)

class Question_Answer_Message(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    qam_id = ShortUUIDField(unique=True, length=6, max_length=30, alphabet='1234567890')
    qa_id = ShortUUIDField(unique=True, length=6, max_length=30, alphabet='1234567890')
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f'{self.user.username} - {self.course.title}'

    class Meta:
        ordering = ['-date']

    def profile(self):
        return Profile.objects.get(user=self.user)

class Cart(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    country = models.CharField(max_length=100, null=True, blank=True)
    cart_id = ShortUUIDField(length=6, max_length=30, alphabet='1234567890')
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return self.course.title

PAYMENT_STATUS = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
)

class CartOrder(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teachers = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    initial_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status = models.CharField(choices=PAYMENT_STATUS, default='pending', max_length=10)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    coupons = models.ManyToManyField('Coupon', blank=True)
    stripe_session_id = models.CharField(max_length=1000, blank=True, null=True)
    oid = ShortUUIDField(unique=True, length=6, max_length=20, alphabet='1234567890')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']
        
    def order_items(self):
        return CartOrderItem.objects.filter(order=self)
    
class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, related_name='order_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_items')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    initial_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    coupons = models.ManyToManyField('Coupon', blank=True)
    applied_coupon = models.BooleanField(default=False)
    oid = ShortUUIDField(unique=True, length=6, max_length=20, alphabet='1234567890')
    date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date']
    
    def order_id(self):
        return f'Order ID # {self.order.oid}'
    
    def payment_status(self):
        return self.oid

class Certificate(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    certificate_id = ShortUUIDField(unique=True, length=6, max_length=30, alphabet='1234567890')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.course.title

class CompletedLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    variant_item = models.ForeignKey(VariantItem, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.course.title

class EnrolledCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='teacher' ,null=True, blank=True)
    enrolled_id = models.DateTimeField(default=timezone.now)
    date = models.DateTimeField(default=timezone.now)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.course.title
    
    def lectures(self):
        return VariantItem.objects.filter(variant__course=self.course)
    
    def completed_lesson(self):
        return CompletedLesson.objects.filter(course=self.course, user=self.user)
    
    def curriculum(self):
        return Variant.objects.filter(course=self.course)
    
    def note(self):
        return Node.objects.get(course=self.course)
    
    def question_answer(self):
        return Question_Answer.objects.filter(course=self.course)
    
    def review(self):
        return Review.objects.filter(course=self.course, user=self.user)

class Note(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField()
    note_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet='1234567890')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING_STATUS, default=None)
    reply = models.CharField(null=True, blank=True, max_length=1000)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return self.course.title
    
    def profile(self):
        return Profile.objects.get(user=self.user)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=100, choices=NOTE_TYPE_CHOICES)  
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return str(self.user)

class Coupon(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    used_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=50)
    discount = models.IntegerField() 
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.code

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.user.username} - {self.course.title}'

class Counter(models.Model):
    name = models.CharField(max_length=500)
    tax_rate = models.IntegerField(default=5)
    active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name
