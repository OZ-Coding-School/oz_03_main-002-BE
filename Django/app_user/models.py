from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string # added common user
# from django.utils import timezone


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
    is_email_verified = models.BooleanField(default=False) # added common user email verified
    email_verification_token = models.CharField(max_length=100, blank=True) # added common user email token
    email = models.EmailField(unique=True)
    )

    USERNAME_FIELD = "user_id"  # user_id를 사용자 이름으로 사용
    REQUIRED_FIELDS = [
        "name",
        "nick_name",
        "password_hash",
        "username",
        'email', # added common login email
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

    # added generate email token
    def generate_email_token(self):
        self.email_verification_token = get_random_string(length=32)
        self.save()
