from django.urls import path

from . import views

urlpatterns = [path("celery/", views.test_celery, name="test_celery")]
