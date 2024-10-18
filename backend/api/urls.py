from api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Authentication 
    path('user/login/', api_views.MyTokenObtainPairView.as_view()),
    path('user/refresh/', TokenRefreshView.as_view()),
    path('user/register/', api_views.RegisterView.as_view()),
    path('user/password-rest-email/<email>', api_views.PasswordRegisterEmailVerifyApiView.as_view()),
    path('user/password-change/', api_views.ChangepasswordApiView.as_view()),
    # core Endpoint
    path('course/category/', api_views.CategoryListAPIView.as_view()),
    path('course/course-list/', api_views.CourseListAPIView.as_view()),
    path('course/course-detail/<slug>/', api_views.CourseDetailApiView.as_view()),
    path('course/cart/', api_views.CartAPIView.as_view()),
    path('course/cart-list/<cart_id>/', api_views.CartAPIView.as_view()),
    path('course/cart-item-delete/<cart_id>/<item_id>/', api_views.CartItemDeleteApiView.as_view()),
    path('cart/stats/<cart_id>/', api_views.CartStatsApiView.as_view()),
    path('order/create-order/', api_views.CreateOrderAPIView.as_view()),
    path('order/checkout/<oid>/', api_views.CheckOutApiView.as_view()),
    path('order/coupon/', api_views.CouponApiView.as_view()),
    path('payment/payment-success/',api_views.PaymentSuccessApiView.as_view()),
    
    
    # student
    path('student/summary/<user_id>/', api_views.StudentSummaryApiView.as_view()),
    path('student/course-list/<user_id>/', api_views.StudentCourseListApiView.as_view()),
    path('student/course-detail/<user_id>/<enrolled_id>/', api_views.StudentCourseDetailApiView.as_view()),
    path('student/course-completed/', api_views.StudentCourseCompletedApiView.as_view()),
    path('student/note/<user_id>/<enrolled_id>/', api_views.StudentNoteApiView.as_view()),
    path('student/note-details/<user_id>/<enrolled_id>/<note_id>/', api_views.StudentNoteDetailApiView.as_view()),
    path('student/course/review/', api_views.StudentCourseRatingApiView.as_view()),
    path('student/course/review/details/<user_id>/<course_id>/', api_views.StudentCourseReviewDetailApiView.as_view()),
    path('student/whish-list/<user_id>/', api_views.StudentWhishListApiView.as_view()),
    path('student/question-answer/question-answer-list-create/<course_id>/', api_views.StudentQuestionAnswerListApiView.as_view()),
    
    
    # Teacher
    path('teacher/summary/<teacher_id>/', api_views.TeacherSummarySerializer.as_view()),
    path('teacher/course-lists/<teacher_id>/', api_views.TeacherCourseListApiView.as_view()),
    path('teacher/review-list/<teacher_id>/', api_views.TeacherReviewListApiView.as_view()),
    path('teacher/review-detail/<teacher_id>/<review_id>/', api_views.TeacherReviewDetailApiView.as_view()),
    
    path('teacher/student-lists/<teacher_id>/', api_views.TeacherStudentsListApiView.as_view({'get':"list"})),
    
    path('teacher/all-month-earning/<teacher_id>/', api_views.TeacherAllMonthlyEarningApiView),
    path('teacher/best-course-earning/<teacher_id>/', api_views.TeacherBestSellingCourseApiView.as_view({'get':"list"})),
    path('teacher/course-order-list/<teacher_id>/', api_views.TeacherCourseOrderListApiView.as_view()),
    path('teacher/question-answer-lists/<teacher_id>/', api_views.TeacherQuestionAnswerListApiView.as_view()),
    path('teacher/coupon-lists/<teacher_id>/', api_views.TeacherCouponListCrateApiView.as_view()),
    path('teacher/coupon-detail/<teacher_id>/<coupon_id>/', api_views.TeacherCouponDetailApiView.as_view()),
    path('teacher/notification-lists/<teacher_id>/', api_views.TeacherNotificationListApiView.as_view()),
    path('teacher/notification-detail/<teacher_id>/<noti_id>/', api_views.TeacherNotificationDetailApiView.as_view()),
]
 