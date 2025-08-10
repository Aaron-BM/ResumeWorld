from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from .views import RegisterUserView

# from rest_framework.routers import DefaultRouter
# from .views import ResumeViewSet

# router = DefaultRouter()
# router.register('resumes', ResumeViewSet, basename='resume')

urlpatterns = []