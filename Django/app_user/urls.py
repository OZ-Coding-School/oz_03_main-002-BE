# app/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "user"

router = DefaultRouter()
router.register("login", views.UserLoginViewSet, basename="user_login")  # UserLoginViewSet 등록
router.register("login", views.UserSignInViewSet, basename="user_signin")  # UserSignInViewSet 등록
router.register(
    "recovery", views.UserAccountRecoveryViewSet, basename="user_recovery"
)  # UserAccountRecoveryViewSet 등록
router.register("login", views.UserRefrigeratorViewSet, basename="user_refrigerator")  # UserRefrigeratorViewSet 등록

urlpatterns = [
    path("", include(router.urls)),
]
