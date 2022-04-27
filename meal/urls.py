from django.urls import path
from . import views

app_name = 'meal'

urlpatterns = [
    path('meal/', views.meal, name='meal'),
    path('meal/upload', views.meal_upload, name='meal_upload'),
    path('meal/del_meal_diet', views.del_meal_diet, name='del_meal_diet'),
    path('meal/food_list', views.food_list, name='food_list'),
    path('meal/search_food_list', views.search_food_list, name='search_food_list'),
    path('meal/meal_diet', views.meal_diet, name='meal_diet'),
]