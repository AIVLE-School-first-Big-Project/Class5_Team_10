from django.urls import path
from . import views

app_name = 'meal'

urlpatterns = [
    path('meal/', views.meal, name='meal'),
    path('meal/upload', views.meal_upload, name='meal_upload'),
    path('meal/del_img', views.del_img, name='del_img'),
    path('meal/food_list', views.food_list, name='food_list'),
    path('meal/search_food_list', views.search_food_list, name='search_food_list'),
]