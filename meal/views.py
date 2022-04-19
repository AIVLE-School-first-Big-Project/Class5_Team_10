from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Meal
from user.models import Kid

# Create your views here.
def meal(request):
    # 있다면 조건문 처리 필요
    meals = Meal.objects.filter(meal_regdate='2022-04-18')
    # print(meals[0].meal_img)
    return render(request, 'meal/meal.html', {'meals': meals})

@csrf_exempt
def meal_upload(request):
    print(request)
    # meal_img = request.FILES.__getitem__('meal_img')
    meal_img = request.POST['meal_img']
    meal_regdate = request.POST['meal_regdate']
    meal_regdate = meal_regdate.replace('. ', '-')
    meal_regdate = meal_regdate.replace('.', '')
    meal_time = request.POST['meal_time']
    print(meal_img)
    
    # 자녀 어떻게 선택?
    kid = Kid.objects.get(kid_id=1)

    m = Meal(meal_img=meal_img, meal_regdate=meal_regdate, meal_time=meal_time, kid_id=kid)
    m.save()

    return render(request, 'meal/meal.html')