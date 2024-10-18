from django.contrib import admin
from . models import User, Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name','date']

class UserAdminPage(admin.ModelAdmin):
    list_display = ['id', 'username']
    
    
admin.site.register(User, UserAdminPage)
admin.site.register(Profile, ProfileAdmin)
