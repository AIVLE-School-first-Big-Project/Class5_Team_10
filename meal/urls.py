from django.urls import path
from . import views

app_name = 'meal'

urlpatterns = [
    path('meal/', views.meal, name='meal'),
    path('meal/upload', views.meal_upload, name='meal_upload')
]