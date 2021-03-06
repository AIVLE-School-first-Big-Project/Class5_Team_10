from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Meal, Nutrition, Diet
from user.models import Kid
import json
import os
import csv
import datetime
from .ai import prediction
from decorators import login_message_required


# meal, diet 객체 가져오기
def get_object(kid, date):
    breakfast_meal = 0
    lunch_meal = 0
    dinner_meal = 0
    breakfast_diet = 0
    lunch_diet = 0
    dinner_diet = 0
    nut_breakfast = 0
    nut_lunch = 0
    nut_dinner = 0

    try:
        breakfast_meal = Meal.objects.filter(kid=kid) &\
            Meal.objects.filter(regdate=date) & Meal.objects.filter(time='아침')
    except Exception:
        pass
    try:
        lunch_meal = Meal.objects.filter(kid=kid) &\
            Meal.objects.filter(regdate=date) & Meal.objects.filter(time='점심')
    except Exception:
        pass
    try:
        dinner_meal = Meal.objects.filter(kid=kid) &\
            Meal.objects.filter(regdate=date) & Meal.objects.filter(time='저녁')
    except Exception:
        pass

    try:
        breakfast_diet = Diet.objects.filter(meal=breakfast_meal[0])
    except Exception:
        pass
    try:
        lunch_diet = Diet.objects.filter(meal=lunch_meal[0])
    except Exception:
        pass
    try:
        dinner_diet = Diet.objects.filter(meal=dinner_meal[0])
    except Exception:
        pass

    try:
        nut_breakfast = Diet.objects.filter(meal__regdate=date) &\
            Diet.objects.filter(meal__kid=kid) &\
            Diet.objects.filter(meal__time='아침')
    except Exception:
        pass
    try:
        nut_lunch = Diet.objects.filter(meal__regdate=date) &\
            Diet.objects.filter(meal__kid=kid) &\
            Diet.objects.filter(meal__time='점심')
    except Exception:
        pass
    try:
        nut_dinner = Diet.objects.filter(meal__regdate=date) &\
            Diet.objects.filter(meal__kid=kid) &\
            Diet.objects.filter(meal__time='저녁')
    except Exception:
        pass

    return breakfast_meal, lunch_meal, dinner_meal,\
        breakfast_diet, lunch_diet, dinner_diet,\
        nut_breakfast, nut_lunch, nut_dinner


# 식단 별 영양성분
def nut_diet(nut_meal):
    intake = {}
    intake['diet'] = [0]*7
    intake['diet_per'] = [0]*7
    energy = 0  # 1400
    carbohydrate = 0  # 180
    protein = 0  # 20
    fat = 0  # 65
    sodium = 0  # 1200
    calcium = 0  # 600
    iron = 0  # 7
    good_food = []
    lack_food = []
    bad_food = []
    good_kcal = 0
    lack_kcal = 0
    bad_kcal = 0

    for nut in nut_meal:
        intake['diet'][0] += nut.nutrition.energy * nut.portions
        intake['diet'][1] += nut.nutrition.carbohydrate * nut.portions
        intake['diet'][2] += nut.nutrition.protein * nut.portions * 0.3
        intake['diet'][3] += nut.nutrition.fat * nut.portions
        intake['diet'][4] += nut.nutrition.sodium * nut.portions * 0.3
        intake['diet'][5] += nut.nutrition.calcium * nut.portions
        intake['diet'][6] += nut.nutrition.iron * nut.portions
        intake['diet_per'][0] +=\
            nut.nutrition.energy * 100 / 1400 * nut.portions
        intake['diet_per'][1] +=\
            nut.nutrition.carbohydrate * 100 / 180 * nut.portions
        intake['diet_per'][2] +=\
            nut.nutrition.protein * 100 / 20 * nut.portions * 0.3
        intake['diet_per'][3] +=\
            nut.nutrition.fat * 100 / 65 * nut.portions
        intake['diet_per'][4] +=\
            nut.nutrition.sodium * 100 / 1200 * nut.portions * 0.3
        intake['diet_per'][5] +=\
            nut.nutrition.calcium * 100 / 600 * nut.portions
        intake['diet_per'][6] += nut.nutrition.iron * 100 / 7 * nut.portions
        energy += nut.nutrition.energy * nut.portions
        carbohydrate += nut.nutrition.carbohydrate * nut.portions
        protein += nut.nutrition.protein * nut.portions * 0.3
        fat += nut.nutrition.fat * nut.portions
        sodium += nut.nutrition.sodium * nut.portions * 0.3
        calcium += nut.nutrition.calcium * nut.portions
        iron += nut.nutrition.iron * nut.portions
    if energy < 1400 * 0.2:
        lack_kcal = round(energy, 2)
    elif 1400 * 0.2 <= energy and energy < 1400 * 0.4:
        good_kcal = round(energy, 2)
    else:
        bad_kcal = round(energy, 2)

    if carbohydrate < 180 * 0.2:
        lack_food.append('탄수화물')
    elif 180 * 0.2 <= carbohydrate and carbohydrate < 180 * 0.4:
        good_food.append('탄수화물')
    else:
        bad_food.append('탄수화물')
    if protein < 20 * 0.2:
        lack_food.append('단백질')
    elif 20 * 0.2 <= protein and protein < 20 * 0.4:
        good_food.append('단백질')
    else:
        bad_food.append('단백질')

    if fat < 65 * 0.2:
        lack_food.append('지방')
    elif 65 * 0.2 <= fat and fat < 65 * 0.4:
        good_food.append('지방')
    else:
        bad_food.append('지방')

    if sodium < 1200 * 0.2:
        lack_food.append('나트륨')
    elif 1200 * 0.2 <= sodium and sodium < 1200 * 0.4:
        good_food.append('나트륨')
    else:
        bad_food.append('나트륨')

    if calcium < 600 * 0.2:
        lack_food.append('칼슘')
    elif 600 * 0.2 <= calcium and calcium < 600 * 0.4:
        good_food.append('칼슘')
    else:
        bad_food.append('칼슘')

    if iron < 7 * 0.2:
        lack_food.append('철분')
    elif 7 * 0.2 <= iron and iron < 7 * 0.4:
        good_food.append('철분')
    else:
        bad_food.append('철분')

    return intake['diet'], intake['diet_per'],\
        lack_kcal, good_kcal, bad_kcal, lack_food, good_food, bad_food


@login_message_required
def meal(request):
    context = {}

    if request.method == "GET":
        # 자녀정보
        try:
            kid_id = request.session['kid_id']
            kid_id = int(kid_id)
            context['kid_id'] = kid_id
            kid = Kid.objects.get(id=kid_id)
        except Exception:
            return redirect('user:kid_select')

        # 오늘 날짜 디폴트
        date = datetime.date.today().strftime('%Y-%m-%d')
        context['date'] = date

        # 영양성분 DB 존재여부
        nutirition = []
        try:
            nutirition = Nutrition.objects.get(food='쌀밥')
        except Exception:
            pass
        if nutirition == []:
            path = 'meal/static/data/nutrition_db.csv'
            file = open(path, 'r', encoding='UTF-8')
            reader = csv.reader(file)
            tmp = []
            for row in reader:
                tmp.append(Nutrition(food=row[0],
                                     quantity=row[1], energy=row[2],
                                     carbohydrate=row[3], sugars=row[4],
                                     fat=row[5],
                                     protein=row[6], calcium=row[7],
                                     phosphorus=row[8],
                                     sodium=row[9], potassium=row[10],
                                     magnesium=row[11], iron=row[12],
                                     zinc=row[13], cholesterol=row[14],
                                     transfat=row[15]))
            Nutrition.objects.bulk_create(tmp)

        try:
            breakfast_meal, lunch_meal, dinner_meal, breakfast_diet,\
                lunch_diet, dinner_diet, nut_breakfast,\
                nut_lunch, nut_dinner = get_object(kid, date)

            if breakfast_meal:
                context['breakfast_meal'] = breakfast_meal
            if lunch_meal:
                context['lunch_meal'] = lunch_meal
            if dinner_meal:
                context['dinner_meal'] = dinner_meal
            if breakfast_diet:
                context['breakfast_diet'] = breakfast_diet
            if lunch_diet:
                context['lunch_diet'] = lunch_diet
            if dinner_diet:
                context['dinner_diet'] = dinner_diet

            intake = {}

            if nut_breakfast:
                intake['breakfast'], intake['breakfast_per'],\
                    lack_kcal_breakfast, good_kcal_breakfast,\
                    bad_kcal_breakfast, lack_food_breakfast,\
                    good_food_breakfast,\
                    bad_food_breakfast = nut_diet(nut_breakfast)
                context['lack_kcal_breakfast'] = lack_kcal_breakfast
                context['good_kcal_breakfast'] = good_kcal_breakfast
                context['bad_kcal_breakfast'] = bad_kcal_breakfast
                context['lack_food_breakfast'] = lack_food_breakfast
                context['good_food_breakfast'] = good_food_breakfast
                context['bad_food_breakfast'] = bad_food_breakfast

            if nut_lunch:
                intake['lunch'], intake['lunch_per'],\
                    lack_kcal_lunch, good_kcal_lunch, bad_kcal_lunch,\
                    lack_food_lunch, good_food_lunch,\
                    bad_food_lunch = nut_diet(nut_lunch)
                context['lack_kcal_lunch'] = lack_kcal_lunch
                context['good_kcal_lunch'] = good_kcal_lunch
                context['bad_kcal_lunch'] = bad_kcal_lunch
                context['lack_food_lunch'] = lack_food_lunch
                context['good_food_lunch'] = good_food_lunch
                context['bad_food_lunch'] = bad_food_lunch

            if nut_dinner:
                intake['dinner'], intake['dinner_per'],\
                    lack_kcal_dinner, good_kcal_dinner, bad_kcal_dinner,\
                    lack_food_dinner, good_food_dinner,\
                    bad_food_dinner = nut_diet(nut_dinner)
                context['lack_kcal_dinner'] = lack_kcal_dinner
                context['good_kcal_dinner'] = good_kcal_dinner
                context['bad_kcal_dinner'] = bad_kcal_dinner
                context['lack_food_dinner'] = lack_food_dinner
                context['good_food_dinner'] = good_food_dinner
                context['bad_food_dinner'] = bad_food_dinner

            j_intake = json.dumps(intake)

            context['intake'] = j_intake
            context['kid'] = kid

            if breakfast_meal or lunch_meal or dinner_meal:
                return render(request, 'meal/meal.html', context=context)
            else:
                return render(request, 'meal/meal.html', context=context)
        except Exception:
            pass
        return render(request, 'meal/meal.html', context=context)

    # 날짜 선택할 경우
    if request.method == "POST":
        kid_id = request.POST.get('kid_id')
        context['kid_id'] = kid_id
        kid = Kid.objects.get(id=kid_id)
        date = request.POST.get('datepicker')
        context['date'] = date
        try:
            breakfast_meal, lunch_meal, dinner_meal,\
                breakfast_diet, lunch_diet, dinner_diet,\
                nut_breakfast, nut_lunch, nut_dinner = get_object(kid, date)

            if breakfast_meal:
                context['breakfast_meal'] = breakfast_meal
            if lunch_meal:
                context['lunch_meal'] = lunch_meal
            if dinner_meal:
                context['dinner_meal'] = dinner_meal
            if breakfast_diet:
                context['breakfast_diet'] = breakfast_diet
            if lunch_diet:
                context['lunch_diet'] = lunch_diet
            if dinner_diet:
                context['dinner_diet'] = dinner_diet

            intake = {}

            if nut_breakfast:
                intake['breakfast'], intake['breakfast_per'],\
                    lack_kcal_breakfast,\
                    good_kcal_breakfast, bad_kcal_breakfast,\
                    lack_food_breakfast, good_food_breakfast,\
                    bad_food_breakfast = nut_diet(nut_breakfast)
                context['lack_kcal_breakfast'] = lack_kcal_breakfast
                context['good_kcal_breakfast'] = good_kcal_breakfast
                context['bad_kcal_breakfast'] = bad_kcal_breakfast
                context['lack_food_breakfast'] = lack_food_breakfast
                context['good_food_breakfast'] = good_food_breakfast
                context['bad_food_breakfast'] = bad_food_breakfast

            if nut_lunch:
                intake['lunch'], intake['lunch_per'], lack_kcal_lunch,\
                    good_kcal_lunch, bad_kcal_lunch,\
                    lack_food_lunch, good_food_lunch,\
                    bad_food_lunch = nut_diet(nut_lunch)
                context['lack_kcal_lunch'] = lack_kcal_lunch
                context['good_kcal_lunch'] = good_kcal_lunch
                context['bad_kcal_lunch'] = bad_kcal_lunch
                context['lack_food_lunch'] = lack_food_lunch
                context['good_food_lunch'] = good_food_lunch
                context['bad_food_lunch'] = bad_food_lunch

            if nut_dinner:
                intake['dinner'], intake['dinner_per'], lack_kcal_dinner,\
                    good_kcal_dinner, bad_kcal_dinner,\
                    lack_food_dinner, good_food_dinner,\
                    bad_food_dinner = nut_diet(nut_dinner)
                context['lack_kcal_dinner'] = lack_kcal_dinner
                context['good_kcal_dinner'] = good_kcal_dinner
                context['bad_kcal_dinner'] = bad_kcal_dinner
                context['lack_food_dinner'] = lack_food_dinner
                context['good_food_dinner'] = good_food_dinner
                context['bad_food_dinner'] = bad_food_dinner

            j_intake = json.dumps(intake)

            context['intake'] = j_intake
            context['kid'] = kid

            if breakfast_meal or lunch_meal or dinner_meal:
                return render(request, 'meal/meal.html', context=context)
            else:
                return render(request, 'meal/meal.html', context=context)
        except Exception:
            pass
        return render(request, 'meal/meal.html', context=context)


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


def meal_diet(request):
    kid_id = request.POST['kid_id']
    try:
        kid = Kid.objects.get(id=kid_id)
    except Exception:
        pass

    meal_regdate = request.POST['date']
    if request.POST['frame'] == 'breakfast_food_form':
        meal_time = '아침'
    elif request.POST['frame'] == 'lunch_food_form':
        meal_time = '점심'
    elif request.POST['frame'] == 'dinner_food_form':
        meal_time = '저녁'

    food_results = request.POST['food_result'].split(',')
    portions = request.POST['portions'].split(',')

    # meal 객체 생성
    meal_img = 0
    try:
        meal_img = request.FILES.__getitem__('meal_img')
    except Exception:
        pass
    if meal_img:
        m = Meal(img=meal_img, regdate=meal_regdate, time=meal_time, kid=kid)
        m.save()
        # diet 객체 생성
        for i in range(len(food_results)):
            if portions[i] == '1인분':
                portions[i] = 1
            elif portions[i] == '0.1인분':
                portions[i] = 0.1
            elif portions[i] == '0.3인분':
                portions[i] = 0.3
            elif portions[i] == '0.5인분':
                portions[i] = 0.5
            elif portions[i] == '0.7인분':
                portions[i] = 0.7
            elif portions[i] == '1.5인분':
                portions[i] = 1.5
            nutrition = Nutrition.objects.get(food=food_results[i])
            d = Diet(meal=m, portions=portions[i], nutrition=nutrition)
            d.save()
    else:
        m = Meal(regdate=meal_regdate, time=meal_time, kid=kid)
        m.save()
        # diet 객체 생성
        for i in range(len(food_results)):
            if portions[i] == '1인분':
                portions[i] = 1
            elif portions[i] == '0.1인분':
                portions[i] = 0.1
            elif portions[i] == '0.3인분':
                portions[i] = 0.3
            elif portions[i] == '0.5인분':
                portions[i] = 0.5
            elif portions[i] == '0.7인분':
                portions[i] = 0.7
            elif portions[i] == '1.5인분':
                portions[i] = 1.5
            nutrition = Nutrition.objects.get(food=food_results[i])
            d = Diet(meal=m, portions=portions[i], nutrition=nutrition)
            d.save()
    return redirect('./')


def del_meal_diet(request):
    req = json.loads(request.body)
    meal_regdate = req['regdate']
    meal_regdate = meal_regdate.replace('. ', '-')
    meal_regdate = meal_regdate.replace('.', '')
    meal_time = req['meal_time']

    kid_id = req['kid_id']
    kid = Kid.objects.get(id=kid_id)

    m = Meal.objects.filter(kid=kid) &\
        Meal.objects.filter(regdate=meal_regdate) &\
        Meal.objects.filter(time=meal_time)
    m.delete()
    try:
        os.remove('media/meal_images/kid_{}/{}_{}{}'
                  .format(kid.id, meal_regdate, meal_time, '.png'))
    except Exception:
        pass

    return render(request, 'meal/meal.html')


def food_list(request):
    foods = Nutrition.objects.all()
    food_name_list = []
    for food in foods:
        food_name_list.append(food.food + ' ')
    return HttpResponse(food_name_list)


def search_food_list(request):
    req = json.loads(request.body)
    search_data = req['search_data']
    foods = Nutrition.objects.filter(food__icontains=search_data)
    food_name_list = []
    for food in foods:
        food_name_list.append(food.food + ' ')
    return HttpResponse(food_name_list)
