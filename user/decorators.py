from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from .models import User
from django.http import HttpResponse

# from functools import wraps
# from urllib.parse import urlparse

# from django.conf import settings
# from django.contrib.auth import REDIRECT_FIELD_NAME
# from django.core.exceptions import PermissionDenied
# from django.shortcuts import resolve_url



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

# def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
#     """
#     Decorator for views that checks that the user is logged in, redirecting
#     to the log-in page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_authenticated,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator