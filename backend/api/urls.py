from api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user/login/", api_views.MyTokenObtainPairView.as_view()),
    path("user/refresh/", TokenRefreshView.as_view()),
    path("user/register/", api_views.RegisterView.as_view()),
    path(
        "user/password-rest-email/<email>",
        api_views.PasswordRegisterEmailVerifyApiView.as_view(),
    ),
    path("user/password-change/", api_views.PasswordChangeApiView.as_view()),
]
