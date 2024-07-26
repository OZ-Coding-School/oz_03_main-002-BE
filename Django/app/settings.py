"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import json
import os
from pathlib import Path

# For Local Test
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%s)3l76c=fst)66im#%_a41(%xe+e7!-%p%vpliulx_-a3(97i"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["43.203.195.173", "127.0.0.1"]


# Application definition

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
CUSTOM_APPS = [
    "django.contrib.postgres",
    "refrigerator",
    "ingredient",
    "recipe",
    "app_user",
    "common",
    # For Redoc
    "rest_framework",
    "drf_yasg",
    # For Swagger
    "rest_framework_swagger",
    # For Login
    "rest_framework_simplejwt",
    #   # Google Social Login
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",  # Google provider 추가
    #   # Common Login
    "common_user",
]


INSTALLED_APPS = DEFAULT_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # # Google Social Login
    "allauth.account.middleware.AccountMiddleware",
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


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "naengttogi",
        "USER": os.environ.get("RDS_USERNAME"),
        "PASSWORD": os.environ.get("RDS_PASSWORD"),
        "HOST": os.environ.get("RDS_HOSTNAME"),
        "PORT": os.environ.get("RDS_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DEFAULT_SCHEMA_CLASS = "rest_framework.schemas.openapi.AutoSchema"
# AUTH_USER_MODEL = "app_user.APP_User"  # 커스텀 사용자 모델 사용 설정

# Swagger
REST_FRAMEWORK = {
    # ... other settings
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    # "SECURITY_DEFINITIONS": {
    #     # 필요에 따라 인증 설정 추가 (예: Basic Authentication, JWT 등)
    # },
}
# ## 로그인 리다이렉트
# LOGIN_URL = "/admin/login/"

# # Google Social Login
# SITE_ID = 1


# # 구글 소셜 로그인
# AUTH_USER_MODEL = "app_user.APP_User"

# 사용할 사이트 갯수
SITE_ID = 1

# REST_USE_JWT = True

# ACCOUNT_USER_MODEL_USERNAME_FIELD = "username" # 유저네임필드 이름
# ACCOUNT_EMAIL_REQUIRED = True # 이메일 사용여부
# ACCOUNT_USERNAME_REQUIRED = True # 유저네임 사용여부
# ACCOUNT_AUTHENTICATION_METHOD = "email" # 인증 필드 메소드
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "APP": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "key": "",
        },
    },
}



# # Common Login
# AUTH_USER_MODEL = "common_user.commonUser" # Added Custom User

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# 이메일 설정
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Gmail SMTP 서버 사용
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # 실제 이메일 주소
EMAIL_HOST_PASSWORD = 'your-email-password'  # 실제 비밀번호 또는 앱 비밀번호



