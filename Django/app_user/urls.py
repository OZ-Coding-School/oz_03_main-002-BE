from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BlacklistTokenUpdateView
from .views import CustomTokenObtainPairView
from .views import CustomTokenRefreshView
from .views import GoogleCallback
from .views import GoogleLogin
from .views import UserInfoView

app_name = "app_user"

router = DefaultRouter()

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
    path("userinfo/", UserInfoView.as_view(), name="userinfo"),
]
