# app/urls.py
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "user"

router = DefaultRouter()
router.register(
    "login", views.UserLoginViewSet, basename="user_login"
)  # UserLoginViewSet 등록
router.register(
    "auth", views.UserSignInViewSet, basename="user_signin"
)  # UserSignInViewSet 등록
router.register(
    "recovery", views.UserAccountRecoveryViewSet, basename="user_recovery"
)  # UserAccountRecoveryViewSet 등록
router.register(
    "refrigerator", views.UserRefrigeratorViewSet, basename="user_refrigerator"
)  # UserRefrigeratorViewSet 등록

urlpatterns = [
    path("", include(router.urls)),
]
