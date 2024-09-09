from api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Authentication 
    path('user/login/', api_views.MyTokenObtainPairView.as_view()),
    path('user/refresh/', TokenRefreshView.as_view()),
    path('user/register/', api_views.RegisterView.as_view()),
    path('user/password-rest-email/<email>', api_views.PasswordRegisterEmailVerifyApiView.as_view()),
    path('user/password-change/', api_views.PasswordChangeApiView.as_view()),
    # core Endpoint
    path('course/category/', api_views.CategoryListAPIView.as_view()),
    path('course/course-list/', api_views.CourseListAPIView.as_view()),
    path('course/course-detail/<slug>/', api_views.CourseDetailApiView.as_view()),
    path('course/cart/', api_views.CartAPIView.as_view()),
    path('course/cart-list/<cart_id>/', api_views.CartAPIView.as_view()),
    path('course/cart-item-delete/<cart_id>/<item_id>/', api_views.CartItemDeleteApiView.as_view()),
    path('cart/stats/<cart_id>/', api_views.CartStatsApiView.as_view()),
]
