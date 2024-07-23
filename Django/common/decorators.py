from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def superuser_required(view_func=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
