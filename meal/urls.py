from django.urls import path
from . import views

app_name = 'meal'

urlpatterns = [
    path('meal/', views.meal, name='meal'),
]