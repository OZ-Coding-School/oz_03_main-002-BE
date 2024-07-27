import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class AppUserManager(BaseUserManager):
    def create_user(self, user_id, email, username, nick_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            user_id=user_id,
            email=self.normalize_email(email),
            username=username,
            nick_name=nick_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, username, nick_name, password=None):
        user = self.create_user(user_id, email, username, nick_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# 사용자 역할 선택
class UserRole(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    USER = "USER", _("User")


# 사용자 모델
class App_User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, max_length=255, unique=True, default=uuid.uuid4
    )  # UUID 형식의 고유 ID
    user_id = models.CharField(
        max_length=255, unique=True
    )  # 로그인에 사용될 사용자 ID (이메일 형식)
    email = models.EmailField(unique=True)  # unique=True 추가
    username = models.CharField(max_length=255)  # 사용자 이름 (이름 + 성)
    nick_name = models.CharField(max_length=255)  # 닉네임
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 시간
    last_login_at = models.DateTimeField(null=True, blank=True)  # 마지막 로그인 시간
    is_active = models.BooleanField(default=True)  # 계정 활성화 여부
    role = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.USER
    )  # 사용자 역할 (ADMIN 또는 USER)
    is_staff = models.BooleanField(default=False)  # 스태프 권한 여부
    date_joined = models.DateTimeField(auto_now_add=True)  # 가입 날짜
    is_superuser = models.BooleanField(default=False)  # 최고 관리자 권한 여부

    objects = AppUserManager()  # CustomUserManager를 사용하도록 설정

    # 사용자 이름 필드 및 필수 필드 설정
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["nick_name", "username", "email"]  # username 필드 추가

    # Django Groups & Permissions 연동
    groups = models.ManyToManyField(
        Group, verbose_name="groups", blank=True, related_name="app_user_set"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        related_name="app_user_set",
    )

    def __str__(self):
        return self.user_id
