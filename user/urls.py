from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.CustomLogin , name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signup/id_check', views.id_check),
    path('register/', views.kid_register, name='kid_register'),
    path('select/', views.kid_select, name='kid_select'),
    path('selected/', views.kid_selected, name='kid_selected'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)