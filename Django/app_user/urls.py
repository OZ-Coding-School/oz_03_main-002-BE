from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import BlacklistTokenUpdateView
from .views import CustomTokenObtainPairView
from .views import CustomTokenRefreshView
from .views import GoogleCallback
from .views import GoogleLogin

app_name = "app_user"

router = DefaultRouter()

# 뷰셋 등록 (로그인, 회원가입, 계정 복구, 냉장고)
router.register(
    "login", views.UserLoginViewSet, basename="user_login"
)  # 로그인 관련 뷰셋
router.register(
    "auth", views.UserSignInViewSet, basename="user_signin"
)  # 회원가입 관련 뷰셋
router.register(
    "recovery", views.UserAccountRecoveryViewSet, basename="user_recovery"
)  # 계정 복구 관련 뷰셋
router.register(
    "refrigerator", views.UserRefrigeratorViewSet, basename="user_refrigerator"
)  # 냉장고 관련 뷰셋

urlpatterns = [
    # 뷰셋 URL 포함
    path("", include(router.urls)),
    # Google OAuth 로그인 관련 URL
    path(
        "google/login/", GoogleLogin.as_view(), name="google_login"
    ),  # GoogleLogin도 클래스 기반 뷰로 변경
    path(
        "google/callback/", GoogleCallback.as_view(), name="google_callback"
    ),  # .as_view() 추가
    # JWT 토큰 관련 URL
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path(
        "token/blacklist/", BlacklistTokenUpdateView.as_view(), name="token_blacklist"
    ),
]
