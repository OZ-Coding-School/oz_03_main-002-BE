# app/urls.py
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
# from .views import CompleteSocialSignupView
# from .views import GoogleLoginCallbackView
from .views import GoogleLoginViewSet, CompleteSocialSignupViewSet

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
########
router.register('google', views.GoogleLoginViewSet, basename='google_login')
router.register('complete-signup', views.CompleteSocialSignupViewSet, basename='complete_social_signup')
########

urlpatterns = [
    path("", include(router.urls)),
    # 구글 소셜로그인
    # path("google/login/", google_login, name="google_login"),
    # path("google/callback/", GoogleLoginCallbackView.as_view(), name="google_callback"),
    # # path('google/login/finish/', CompleteSocialSignupView.as_view(), name='google_login_todjango'),
    # path(
    #     "complete_social_signup/",
    #     CompleteSocialSignupView.as_view(),
    #     name="complete_social_signup",
    # ),  # 추가 정보 입력 폼 URL 패턴
]



