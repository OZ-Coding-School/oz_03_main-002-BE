from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.

import secrets

class Common_user(AbstractUser):

    def create_user(self, email, username, nickname, password=None):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, nickname, password):
        user = self.create_user(email, username, nickname, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


    class Common_user(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, unique=True)
    nickname = models.CharField(_('nickname'), max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = Common_userManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nickname']

    def __str__(self):
        return self.email

# Create Token
    class EmailVerificationToken(models.Model):
        user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
        token = models.CharField(max_length=64, unique=True)
        created_at = models.DateTimeField(auto_now_add=True)

        def save(self, *args, **kwargs):
            if not self.token:
                self.token = secrets.token_urlsafe(32)
            super().save(*args, **kwargs)

        def is_valid(self):
            return (timezone.now() - self.created_at).days < 1
