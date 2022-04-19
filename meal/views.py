from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Meal
from user.models import Kid

# Create your views here.
def meal(request):
    # 있다면 조건문 처리 필요
    # 자녀, 날짜 어떻게 선택?
    kid = Kid.objects.get(id=2)
    meals = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate='2022-04-19')
    if meals:
        return render(request, 'meal/meal.html', {'meals': meals})
    else:
        return render(request, 'meal/meal.html')

@csrf_exempt
def meal_upload(request):
    print(request)
    meal_img = request.FILES.__getitem__('meal_img')
    meal_regdate = request.POST['meal_regdate']
    meal_regdate = meal_regdate.replace('. ', '-')
    meal_regdate = meal_regdate.replace('.', '')
    meal_time = request.POST['meal_time']
    print(meal_img)
    
    # 자녀 어떻게 선택?
    kid = Kid.objects.get(id=2)

    m = Meal(img=meal_img, regdate=meal_regdate, time=meal_time, kid=kid)
    m.save()

    return redirect('./')