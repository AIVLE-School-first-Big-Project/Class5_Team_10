from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


# 로그인 확인
def login_message_required(function=None):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "로그인한 사용자만 이용할 수 있습니다.")
            return redirect(settings.LOGIN_URL)
        return function(request, *args, **kwargs)
    return wrap


# 비로그인 확인
def logout_message_required(function=None):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "접속중인 사용자입니다.")
            return redirect('/')
        return function(request, *args, **kwargs)
    return wrap


# 관리자 권한 확인
def staff_member_required(view_func=None,
                          redirect_field_name=REDIRECT_FIELD_NAME,
                          login_url='user:login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
