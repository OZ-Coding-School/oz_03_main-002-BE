import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework_simplejwt.tokens import OutstandingToken
from cryptography.fernet import Fernet


class AppUserManager(BaseUserManager):
    """
    사용자 모델 관리자: 사용자 생성 및 슈퍼유저 생성 기능을 제공합니다.
    """
    def create_user(self, user_id, email, username, nick_name, password=None):
        """
        일반 사용자 생성
        """
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
        """
        슈퍼유저 생성
        """
        user = self.create_user(user_id, email, username, nick_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserRole(models.TextChoices):
    """
    사용자 역할 선택: ADMIN, USER
    """

    ADMIN = "ADMIN", _("관리자")
    USER = "USER", _("사용자")


class App_User(AbstractBaseUser, PermissionsMixin):
    """
    사용자 모델: 사용자 정보를 저장합니다.
    """

    id = models.UUIDField(primary_key=True, max_length=255, unique=True, default=uuid.uuid4)
    user_id = models.CharField(max_length=255, unique=True, editable=False)  # 로그인 ID (이메일 형식)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 시간
    last_login_at = models.DateTimeField(null=True, blank=True)  # 마지막 로그인 시간
    is_active = models.BooleanField(default=True)  # 계정 활성화 여부
    role = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.USER
    )
    is_staff = models.BooleanField(default=False)  # 스태프 권한
    date_joined = models.DateTimeField(auto_now_add=True)  # 가입일
    is_superuser = models.BooleanField(default=False)  # 최고 관리자 권한
    refresh_token = models.TextField(blank=True, null=True)  # 리프레시 토큰 저장 필드

    objects = AppUserManager()  # 커스텀 사용자 관리자 사용

    USERNAME_FIELD = "user_id"  # 로그인에 사용할 필드
    REQUIRED_FIELDS = ["nick_name", "username", "email"]

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

    def encrypt_refresh_token(self, refresh_token):
        """
        리프레시 토큰 암호화
        """
        fernet = Fernet(settings.ENCRYPTION_KEY)
        return fernet.encrypt(refresh_token.encode()).decode()

    def decrypt_refresh_token(self):
        """
        리프레시 토큰 복호화
        """
        if self.refresh_token:
            fernet = Fernet(settings.ENCRYPTION_KEY)
            return fernet.decrypt(self.refresh_token.encode()).decode()
        return None

    def __str__(self):
        return self.user_id


# --- SimpleJWT 관련 ---
class OutstandingToken(models.Model):
    """
    발급된 JWT 토큰 모델: SimpleJWT의 OutstandingToken 모델을 상속받아 커스텀합니다.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field="id",
        related_name="outstanding_tokens",
    )

    class Meta:
        abstract = False  # 데이터베이스에 테이블 생성
