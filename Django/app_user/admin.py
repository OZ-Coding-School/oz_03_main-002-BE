from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import App_User


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = App_User
        fields = "__all__"
        exclude = ("date_joined",)  # date_joined 필드 제외


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm  # 수정된 폼 사용
    fieldsets = (
        (None, {"fields": ("user_id", "password")}),
        (("Personal info"), {"fields": ("username", "nick_name", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login",)}),  # date_joined 제거
    )
    list_display = ("id", "user_id", "username", "nick_name", "is_staff")
    search_fields = ("id", "user_id", "username", "nick_name")
    ordering = ("-date_joined",)  # 최근 가입 순으로 정렬


admin.site.register(App_User, CustomUserAdmin)
