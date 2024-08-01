from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


def superuser_required(view_func=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser, login_url=login_url
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def custom_superuser_required(view_func=None, login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({"error": "로그인이 필요합니다."}, status=401)
            if not request.user.is_superuser:
                return Response(
                    {"error": "관리자 권한이 필요합니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            return view_func(self, request, *args, **kwargs)

        return _wrapped_view

    if view_func:
        return decorator(view_func)
    return decorator


def login_required_ajax(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):  # self 인자 추가
        if not request.user.is_authenticated:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=401)
        return view_func(self, request, *args, **kwargs)  # self 인자 전달

    return wrapper
