from api import views as api_views 
from django.urls import path

urlpatterns = [
    path('user/token/',api_views.MyTokenObtainPairView.as_view())
]
