from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'user'

urlpatterns = [
    # 로그인 로그아웃
    path('login/', views.CustomLogin, name='login'),
    path('logout/', views.CustomLogout, name='logout'),
    # 회원가입
    path('signup/', views.signup, name='signup'),
    path('signup/id_check', views.id_check),
    # 유저 정보 수정, 삭제
    path('update/my_info/', views.user_update, name='user_update'),
    path('member_del/', views.member_del, name='member_del'),
    path('id_reset/', views.ForgotIDView, name='forgot_id'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # 아이 정보 등록, 수정, 삭제
    path('register/', views.kid_register, name='kid_register'),
    path('kid_del/', views.kid_del, name='kid_del'),
    path('update/kid_info/', views.kid_update_each, name='kid_update'),
    # 아이 선택
    path('select_kid/', views.kid_select, name='kid_select'),
    path('select_kid/kid', views.kid_send, name='kid'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
