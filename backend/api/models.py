from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from account.models import User
from shortuuid.django_fields import ShortUUIDField

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='course-file', blank=True, null=True, default='course.jpg')
    full_name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    counter = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.full_name
    

class Category(models.Model):
    title = models.CharField(max_length=255)
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
            
LANGUAGE_CHOICES = (
    ('English', 'English'),
    ('Dari', 'Dari'),
    ('Pashto', 'Pashto'),
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
    course_id = ShortUUIDField(unique=True, max_length=30, length=6, alphabet='1234567890')
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
