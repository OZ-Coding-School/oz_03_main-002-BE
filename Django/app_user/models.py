from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    USER = "USER", _("User")


class App_User(AbstractUser):
    user_id = models.CharField(max_length=255, unique=True)  # user_id 필드 추가
    password_hash = models.CharField(max_length=255)
    name = models.CharField(max_length=255)  # name 필드 추가
    nick_name = models.CharField(max_length=255)  # nick_name 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    is_activate = models.BooleanField(default=True)
    role = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.USER
    )

    USERNAME_FIELD = "user_id"  # user_id를 사용자 이름으로 사용
    REQUIRED_FIELDS = [
        "name",
        "nick_name",
        "password_hash",
        "username",
    ]  # 필수 필드 설정
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
