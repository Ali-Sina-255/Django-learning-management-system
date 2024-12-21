from apps.api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user/login/", api_views.MyTokenObtainPairView.as_view()),
    path("user/token/refresh/", TokenRefreshView.as_view()),
    path("user/register/", api_views.RegisterView.as_view()),
    path(
        "user/password-rest-email/<email>/",
        api_views.PasswordRegisterEmailVerifyApiView.as_view(),
    ),
    path("user/password-change/", api_views.PasswordChangeApiView.as_view()),
    path("course/course-list/", api_views.CourseListAPIView.as_view()),
    path("course/course-detail/", api_views.CourseDetailApiView.as_view()),
]
