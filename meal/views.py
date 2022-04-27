from gzip import READ
from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Meal, Nutrition, Diet
from user.models import Kid
import json, os, csv, datetime
from .ai import prediction

@csrf_exempt
def meal(request):
    context = {}
    # 자녀, 날짜 어떻게 선택?
    kid = Kid.objects.get(id=1)

    if request.method == "GET":
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

        date = datetime.date.today().strftime('%Y-%m-%d')
        context['date'] = date
        try:
            morning_meal = 0
            lunch_meal = 0
            evening_meal = 0
            morning_diet = 0
            lunch_diet = 0
            evening_diet = 0

            try: morning_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=date) & Meal.objects.filter(time='아침')
            except: pass
            try: lunch_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=date) & Meal.objects.filter(time='점심')
            except: pass
            try: evening_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=date) & Meal.objects.filter(time='저녁')
            except: pass

            try: morning_diet = Diet.objects.filter(meal=morning_meal[0])
            except: pass
            try: lunch_diet = Diet.objects.filter(meal=lunch_meal[0])
            except: pass
            try: evening_diet = Diet.objects.filter(meal=evening_meal[0])
            except: pass

            if morning_meal: context['morning_meal'] = morning_meal
            else: pass
            if lunch_meal: context['lunch_meal'] = lunch_meal
            else: pass
            if evening_meal: context['evening_meal'] = evening_meal
            else: pass
            if morning_diet: context['morning_diet'] = morning_diet
            else: pass
            if lunch_diet: context['lunch_diet'] = lunch_diet
            else: pass
            if evening_diet: context['evening_diet'] = evening_diet
            else: pass

            if morning_meal or lunch_meal or evening_meal:
                return render(request, 'meal/meal.html', context=context)
            else:
                return render(request, 'meal/meal.html', {'date': date})
        except: pass
        return render(request, 'meal/meal.html', {'date': date})

    # 날짜 선택할 경우
    if request.method == "POST":
        date = request.POST.get('datepicker')
        context['date'] = date
        try:
            morning_meal = 0
            lunch_meal = 0
            evening_meal = 0
            morning_diet = 0
            lunch_diet = 0
            evening_diet = 0

            try: morning_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=date) & Meal.objects.filter(time='아침')
            except: pass
            try: lunch_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=date) & Meal.objects.filter(time='점심')
            except: pass
            try: evening_meal = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=date) & Meal.objects.filter(time='저녁')
            except: pass

            try: morning_diet = Diet.objects.filter(meal=morning_meal[0])
            except: pass
            try: lunch_diet = Diet.objects.filter(meal=lunch_meal[0])
            except: pass
            try: evening_diet = Diet.objects.filter(meal=evening_meal[0])
            except: pass

            if morning_meal: context['morning_meal'] = morning_meal
            else: pass
            if lunch_meal: context['lunch_meal'] = lunch_meal
            else: pass
            if evening_meal: context['evening_meal'] = evening_meal
            else: pass
            if morning_diet: context['morning_diet'] = morning_diet
            else: pass
            if lunch_diet: context['lunch_diet'] = lunch_diet
            else: pass
            if evening_diet: context['evening_diet'] = evening_diet
            else: pass

            if morning_meal or lunch_meal or evening_meal:
                return render(request, 'meal/meal.html', context=context)
            else:
                return render(request, 'meal/meal.html', {'date': date})
        except: pass
        return render(request, 'meal/meal.html', {'date': date})

@csrf_exempt
def meal_upload(request):
    meal_img = request.FILES.__getitem__('meal_img')

    # ai 모델 적용
    ai_result = prediction(meal_img)
    foods = list(set(ai_result['names']))
    foods_len = len(foods)
    results = []
    for food in foods:
        results.append(food + ', ')
    results.append(str(foods_len))
    return HttpResponse(results)

@csrf_exempt
def meal_diet(request):
    # 자녀 어떻게 선택?
    kid = Kid.objects.get(id=1)

    meal_regdate = request.POST['date']
    if request.POST['frame'] == 'morning_food_form': meal_time = '아침'
    elif request.POST['frame'] == 'lunch_food_form': meal_time = '점심'
    elif request.POST['frame'] == 'evening_food_form': meal_time = '저녁'

    food_results = request.POST['food_result'].split(',')
    portions = request.POST['portions'].split(',')

    # meal 객체 생성
    meal_img = 0
    try:
        meal_img = request.FILES.__getitem__('meal_img')
    except: pass
    if meal_img:
        m = Meal(img=meal_img, regdate=meal_regdate, time=meal_time, kid=kid)
        m.save()
        # diet 객체 생성
        for i in range(len(food_results)):
            if portions[i] == '1인분': portions[i] = 1
            elif portions[i] == '0.5인분': portions[i] = 0.5
            elif portions[i] == '1.5인분': portions[i] = 1.5
            nutrition = Nutrition.objects.get(food=food_results[i])
            d = Diet(meal=m, portions=portions[i], nutrition=nutrition)
            d.save()
    else:
        m = Meal(regdate=meal_regdate, time=meal_time, kid=kid)
        m.save()
        # diet 객체 생성
        for i in range(len(food_results)):
            if portions[i] == '1인분': portions[i] = 1
            elif portions[i] == '0.5인분': portions[i] = 0.5
            elif portions[i] == '1.5인분': portions[i] = 1.5
            nutrition = Nutrition.objects.get(food=food_results[i])
            d = Diet(meal=m, portions=portions[i], nutrition=nutrition)
            d.save()

    # ----------------------------------------------------------------------------

    # # 음식에 대한 영양소
    # for food in range(len(food_list)):
    #     nutrition = Nutrition.objects.get(food=food_list[food])
    #     print(nutrition)
    #     print(nutrition.fat)  # 해당 음식의 지방

    # return render(request, 'meal/meal.html') 
    return redirect('./') 

@csrf_exempt
def del_meal_diet(request):
    req = json.loads(request.body)
    meal_regdate = req['regdate']
    meal_regdate = meal_regdate.replace('. ', '-')
    meal_regdate = meal_regdate.replace('.', '')
    meal_time = req['meal_time']

    # 자녀 어떻게 선택?
    kid = Kid.objects.get(id=1)
    m = Meal.objects.filter(kid=kid) & Meal.objects.filter(regdate=meal_regdate) & Meal.objects.filter(time=meal_time)
    m.delete()
    try: os.remove('media/meal_images/kid_{}/{}_{}{}'.format(kid.id, meal_regdate, meal_time, '.png'))
    except: pass

    return render(request, 'meal/meal.html')

@csrf_exempt
def food_list(request):
    foods = Nutrition.objects.all()
    food_name_list = []
    for food in foods:
        food_name_list.append(food.food + ' ')
    return HttpResponse(food_name_list)


@csrf_exempt
def search_food_list(request):
    req = json.loads(request.body)
    search_data = req['search_data']
    foods = Nutrition.objects.filter(food__icontains=search_data)
    food_name_list = []
    for food in foods:
        food_name_list.append(food.food + ' ')
    return HttpResponse(food_name_list)
