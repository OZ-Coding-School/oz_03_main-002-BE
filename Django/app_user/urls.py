# app/urls.py
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (UserRegistrationView, UserLoginView, EmailVerificationView,
                    PasswordResetRequestView, PasswordResetConfirmView, UserLogoutView) # import added common user

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
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    # added common login user-register path
    path('login/', UserLoginView.as_view(), name='user-login'),
    # added common login user-login path
    path('verify-email/<str:token>/', EmailVerificationView.as_view(), name='verify-email'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
]
