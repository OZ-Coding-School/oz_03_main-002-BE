from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import App_User, OutstandingToken


class CustomUserChangeForm(UserChangeForm):
    """
    사용자 정보 변경 폼: 비밀번호 필드를 읽기 전용으로 변경합니다.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = App_User
        fields = "__all__"
        exclude = ("date_joined",)  # date_joined 필드 제외


class CustomUserAdmin(UserAdmin):
    """
    사용자 관리 페이지 커스터마이징
    """
    form = CustomUserChangeForm  # 사용자 정의 폼 사용
    fieldsets = (
        (None, {"fields": ("user_id", "password")}),
        ("개인 정보", {"fields": ("username", "nick_name", "email")}),
        (
            "권한",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("중요 날짜", {"fields": ("last_login",)}),  # date_joined 제거
    )
    list_display = ("id", "user_id", "username", "nick_name", "is_staff")
    search_fields = ("id", "user_id", "username", "nick_name")
    ordering = ("-date_joined",)  # 최근 가입 순으로 정렬


class OutstandingTokenAdmin(admin.ModelAdmin):
    """
    발급된 토큰 관리 페이지
    """

    list_display = ("user_id", "token_str")
    search_fields = ("user_id", "token")

    def token_str(self, obj):
        """
        토큰 값을 문자열로 표시
        """
        return str(obj.token)

    token_str.short_description = "Token"

    def user_id(self, obj):
        """
        user_id 값을 표시
        """
        return obj.user.user_id

    user_id.short_description = "user_id"


# Django Admin에 모델 등록
admin.site.register(App_User, CustomUserAdmin)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
