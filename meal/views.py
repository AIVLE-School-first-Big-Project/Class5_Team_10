from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Meal
from user.models import Kid
import json, os

# Create your views here.
def meal(request):
    # 있다면 조건문 처리 필요
    # 자녀, 날짜 어떻게 선택?
    kid = Kid.objects.get(id=2)
    morning_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate='2022-04-20') & Meal.objects.filter(time='아침')
    lunch_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate='2022-04-20') & Meal.objects.filter(time='점심')
    evening_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate='2022-04-20') & Meal.objects.filter(time='저녁')
    if morning_meal or lunch_meal or evening_meal:
        return render(request, 'meal/meal.html', {'morning_meal': morning_meal, 'lunch_meal': lunch_meal, 'evening_meal': evening_meal})
        # return redirect('./', {'meals': meals})
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
    
    # 자녀 어떻게 선택?
    kid = Kid.objects.get(id=2)

    m = Meal(img=meal_img, regdate=meal_regdate, time=meal_time, kid=kid)
    m.save()

    # return render(request, 'meal/meal.html')
    return redirect('./')
    # return HttpResponseRedirect('./')

@csrf_exempt
def del_img(request):
    req = json.loads(request.body)
    meal_regdate = req['regdate']
    meal_regdate = meal_regdate.replace('. ', '-')
    meal_regdate = meal_regdate.replace('.', '')
    meal_time = req['meal_time']
    print(meal_regdate, meal_time)

    # 자녀 어떻게 선택?
    kid = Kid.objects.get(id=2)
    m = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=meal_regdate) & Meal.objects.filter(time=meal_time)
    m.delete()
    try:
        os.remove('media/meal_images/kid_{}/{}_{}{}'.format(kid.id, meal_regdate, meal_time, '.png'))
    except: pass

    # return redirect('./')
    return render(request, 'meal/meal.html')