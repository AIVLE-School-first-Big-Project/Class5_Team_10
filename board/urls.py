from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'board'

urlpatterns = [
    path('',  views.post_list, name='post_list'),
    path('<int:post_id>/',  views.post, name='post'),
    path('post/create/', views.post_create, name='post_create')
]