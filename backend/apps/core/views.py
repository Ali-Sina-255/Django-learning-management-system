import time

from django.http import HttpResponse
from django.shortcuts import render

from .tasks import celery_test_task


def test_celery(request):
    celery_test_task.delay()
    return HttpResponse("Welcome to celery")
