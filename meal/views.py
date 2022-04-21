from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Meal, Nutrition
from user.models import Kid
import json, os, csv

# Create your views here.
def meal(request):
    # nutrition db가 없으면 추가(csv_to_model)
    nutirition = []
    try: nutirition = Nutrition.objects.get(food='쌀밥')
    except: pass
    if nutirition == []:
        path = 'meal/static/data/nutrition_db.csv'
        file = open(path, 'r', encoding='UTF-8')
        reader = csv.reader(file)
        tmp = []
        
        for row in reader:
            tmp.append(Nutrition(food=row[0], quantity=row[1], energy=row[2],\
                carbohydrate=row[3], sugars=row[4], fat=row[5],\
                    protein=row[6], calcium=row[7], phosphorus=row[8],\
                        sodium=row[9], potassium=row[10], magnesium=row[11],\
                            iron=row[12], zinc=row[13], cholesterol=row[14],\
                                transfat=row[15]))
        Nutrition.objects.bulk_create(tmp)


    # 있다면 조건문 처리 필요
    # 자녀, 날짜 어떻게 선택?
    try:
        kid = Kid.objects.get(id=2)
        regdata = '2022-04-22'
        morning_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=regdata) & Meal.objects.filter(time='아침')
        lunch_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=regdata) & Meal.objects.filter(time='점심')
        evening_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=regdata) & Meal.objects.filter(time='저녁')
        if morning_meal or lunch_meal or evening_meal:
            return render(request, 'meal/meal.html', {'morning_meal': morning_meal, 'lunch_meal': lunch_meal, 'evening_meal': evening_meal})
            # return redirect('./', {'meals': meals})
        else:
            return render(request, 'meal/meal.html')
    except: pass
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
    try: os.remove('media/meal_images/kid_{}/{}_{}{}'.format(kid.id, meal_regdate, meal_time, '.png'))
    except: pass

    # return redirect('./')
    return render(request, 'meal/meal.html')

@csrf_exempt
def nutrition_list(request):
    return render(request, 'meal/meal.html')
