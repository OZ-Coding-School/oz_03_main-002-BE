import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Django 기본 설정
BASE_DIR = Path(__file__).resolve().parent.parent  # 프로젝트 루트 디렉토리
SECRET_KEY = os.environ.get("SECRET_KEY")  # 암호화 키 (반드시 비밀 유지)
DEBUG = os.environ.get(
    "DEBUG", default=False
)  # 개발 모드 (True) 또는 배포 모드 (False)
ALLOWED_HOSTS = [os.environ.get("IPv4")]  # 접근 허용 호스트

# 애플리케이션 목록 (Django 기본 앱 및 프로젝트 앱)
INSTALLED_APPS = [
    # Django 기본 앱
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # 써드파티 앱 (API 관련)
    "django.contrib.postgres",  # PostgreSQL 데이터베이스 사용 시
    "rest_framework",  # Django REST framework (API 개발)
    "drf_yasg",  # API 문서 자동 생성 (Swagger/Redoc)
    "rest_framework_swagger",  # Swagger UI
    "rest_framework_simplejwt",  # JWT 토큰 인증
    "rest_framework.authtoken",  # 기본 토큰 인증 (필요 시)
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",  # CORS (Cross-Origin Resource Sharing) 처리
    # 프로젝트 앱
    "refrigerator",  # 냉장고 관련 앱
    "ingredient",  # 식재료 관련 앱
    "recipe",  # 레시피 관련 앱
    "app_user",  # 사용자 관련 앱
    "common",  # 공통 기능 앱
]

# 미들웨어 설정 (CORS 미들웨어 추가)
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS 미들웨어 (반드시 가장 먼저 위치)
    "django.middleware.security.SecurityMiddleware",  # 보안 관련 미들웨어
    "django.contrib.sessions.middleware.SessionMiddleware",  # 세션 미들웨어
    "django.middleware.common.CommonMiddleware",  # 공통 미들웨어
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF 방지 미들웨어
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # 인증 미들웨어
    "django.contrib.messages.middleware.MessageMiddleware",  # 메시지 미들웨어
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # 클릭재킹 방지 미들웨어
]

ROOT_URLCONF = "app.urls"  # URL 설정 파일 경로

# 템플릿 설정 (사용하지 않을 경우 생략 가능)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates"
        ],  # 템플릿 디렉토리 설정 (사용하지 않을 경우 생략 가능)
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # 디버그 정보
                "django.template.context_processors.request",  # 요청 객체
                "django.contrib.auth.context_processors.auth",  # 사용자 인증 정보
                "django.contrib.messages.context_processors.messages",  # 메시지 정보
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"  # WSGI 애플리케이션 설정

# 데이터베이스 설정 (PostgreSQL 사용 예시)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("RDS_USERNAME"),  # 데이터베이스 이름 (환경 변수 사용)
        "USER": os.environ.get("RDS_USERNAME"),  # 데이터베이스 사용자 (환경 변수 사용)
        "PASSWORD": os.environ.get(
            "RDS_PASSWORD"
        ),  # 데이터베이스 비밀번호 (환경 변수 사용)
        "HOST": os.environ.get("RDS_HOSTNAME"),  # 데이터베이스 호스트 (환경 변수 사용)
        "PORT": os.environ.get("RDS_PORT"),  # 데이터베이스 포트 (환경 변수 사용)
        "CONN_MAX_AGE": 3600,  # 데이터베이스 연결 유지 시간 (초 단위)
    }
}

# 비밀번호 유효성 검사 설정
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 국제화 설정
LANGUAGE_CODE = "ko-kr"  # 한국어 설정
TIME_ZONE = "Asia/Seoul"  # 한국 시간대 설정
USE_I18N = True
USE_TZ = True

# 정적 파일 설정
STATIC_URL = "static/"  # 정적 파일 URL (기본값)

# 사용자 모델 설정 (app_user 앱의 App_User 모델 사용)
AUTH_USER_MODEL = "app_user.App_User"

# Django REST framework 설정 (JWT 인증 추가)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SITE_ID = 1

# Google OAuth 설정 (클라이언트 ID, 시크릿 키)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# Simple JWT 설정 (액세스 토큰 및 리프레시 토큰 만료 시간 설정)
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # 액세스 토큰 만료 시간 (30분)
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=2),  # 리프레시 토큰 만료 시간 (2시간)
    "ROTATE_REFRESH_TOKENS": True,  # 리프레시 토큰 순환 비활성화 (권장)
    "BLACKLIST_AFTER_ROTATION": True,  # 리프레시 토큰 순환 시 기존 토큰 블랙리스트 추가
    "AUTH_COOKIE": "access_token",  # 액세스 토큰을 저장할 쿠키 이름 (기본값: access)
    "AUTH_COOKIE_SECURE": False,  # HTTPS를 사용하지 않는 경우 False로 설정
    "AUTH_COOKIE_HTTP_ONLY": True,  # JavaScript에서 쿠키 접근 불가 (보안 강화)
    "AUTH_COOKIE_PATH": "/",  # 쿠키 경로 설정 (필요에 따라 변경)
    "AUTH_COOKIE_SAMESITE": "Lax",
    "USER_ID_CLAIM": "user_id",
}

# 암호화 키 (리프레시 토큰 암호화에 사용)
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")


GOOGLE_CALLBACK_URI = (
    "http://" + os.environ.get("IPv4") + ":8000/api/v1/google/callback/"
)


CORS_ORIGIN_ALLOW_ALL = False  # 비활성화
CORS_ALLOWED_ORIGINS = [
    "http://" + os.environ.get("IPv4") + ":3000",  # 프론트엔드 주소 (개발 환경)
    "http://" + os.environ.get("IPv4") + ":8000",  # 백엔드 주소 (개발 환경)
    # 실제 배포 환경의 프론트엔드 주소를 추가해야 합니다.
]
CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_DOMAIN = os.environ.get("IPv4")  # 실제 도메인으로 변경
SESSION_COOKIE_PATH = "/"
