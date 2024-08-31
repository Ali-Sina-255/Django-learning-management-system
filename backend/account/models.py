from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import signals

class User(AbstractUser):
	username = models.CharField(max_length=255)
	full_name = models.CharField(max_length=255)
	email = models.EmailField(max_length=200, unique=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	
	def __str__(self) -> str:
		return self.username


	def save(self, *args, **kwargs):
		email_username, full_name = self.email.split("@")
		if self.first_name == "" or self.full_name == None:
			self.first_name == email_username
   
		if self.username == "" or self.username == None:
			self.username = self.email_user
		super(User,self).save(*args, **kwargs)
  

class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	images = models.ImageField(upload_to='user-folder', default='default-profile',null=True, blank=True)
	country = models.CharField(max_length=200, null=True, blank=True)
	full_name = models.CharField(max_length=255)
	bio = models.TextField(null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	
	def __str__(self) -> str:
		if self.full_name:
			return str(self.full_name)
		else:
			return str(self.user.full_name)	

	def save(self, *args, **kwargs):
		if self.full_name == '' or self.full_name == None:
			self.full_name == self.user.username
		super(Profile, self).save(*args, **kwargs)