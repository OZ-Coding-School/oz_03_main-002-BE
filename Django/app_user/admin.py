from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import App_User


class CustomUserAdmin(UserAdmin):
    # 기본 UserAdmin 클래스를 상속하고 필요에 따라 커스터마이징합니다.
    fieldsets = (
        (None, {"fields": ("user_id", "password")}),
        (("Personal info"), {"fields": ("name", "nick_name", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("id", "user_id", "username", "nick_name", "is_staff")
    search_fields = ("id", "user_id", "username", "nick_name")
    ordering = ("-date_joined",)  # 최근 가입 순으로 정렬


admin.site.register(App_User, CustomUserAdmin)
