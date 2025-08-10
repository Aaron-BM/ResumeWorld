from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from resume.views import ResumeViewSet, RegisterUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register('resumes', ResumeViewSet, basename='resume')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path('register/',RegisterUserView.as_view(), name='register'),
]

urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)