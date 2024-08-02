import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# settings.py

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "app_user": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "refrigerator": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "common": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "rest_framework_simplejwt": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


# Django 기본 설정
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# 애플리케이션 목록
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.postgres",
    "rest_framework",
    "drf_yasg",
    "rest_framework_swagger",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "refrigerator",
    "ingredient",
    "recipe",
    "app_user",
    "common",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# 데이터베이스 설정
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

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

AUTH_USER_MODEL = "app_user.App_User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SITE_ID = 1

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")

GOOGLE_CALLBACK_URI = f"https://{os.environ.get('HOST')}/api/v1/google/callback/"
# GOOGLE_CALLBACK_URI = (
#     f"http://127.0.0.1:8000/api/v1/google/callback/"  # 로컬 개발시 환경
# )

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")

SESSION_COOKIE_DOMAIN = os.environ.get("SESSION_COOKIE_DOMAIN")
SESSION_COOKIE_PATH = "/"


SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "DEFAULT_API_AUTHENTICATION": "Bearer",  # Bearer 인증 기본값으로 설정
    "USE_SESSION_AUTH": False,  # 세션 인증 비활성화 (JWT 사용 시)
    "JSON_EDITOR": True,  # JSON 형식 편집기 활성화 (선택 사항)
}
