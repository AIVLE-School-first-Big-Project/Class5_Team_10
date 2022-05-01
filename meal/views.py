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

    if request.method == "GET":
        # 자녀정보
        try:
            kid_id = request.session['kid_id']
            kid_id = int(kid_id)
            context['kid_id'] = kid_id
            kid = Kid.objects.get(id=kid_id)
        except: pass

        # 오늘 날짜 디폴트
        date = datetime.date.today().strftime('%Y-%m-%d')
        context['date'] = date

        # 영양성분 DB 존재여부
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

            nut_breakfast = 0
            nut_lunch = 0
            nut_dinner = 0
            try: nut_breakfast = Diet.objects.filter(meal__regdate=date) & Diet.objects.filter(meal__kid=kid) & Diet.objects.filter(meal__time='아침')
            except: pass
            try: nut_lunch = Diet.objects.filter(meal__regdate=date) & Diet.objects.filter(meal__kid=kid) & Diet.objects.filter(meal__time='점심')
            except: pass
            try: nut_dinner = Diet.objects.filter(meal__regdate=date) & Diet.objects.filter(meal__kid=kid) & Diet.objects.filter(meal__time='저녁')
            except: pass

            intake2 = {}
            intake2['breakfast'] = [0]*7
            intake2['lunch'] = [0]*7
            intake2['dinner'] = [0]*7
            intake2['breakfast_per'] = [0]*7
            intake2['lunch_per'] = [0]*7
            intake2['dinner_per'] = [0]*7

            if nut_breakfast:
                energy = 0  # 2000
                carbohydrate = 0  # 300
                protein = 0  # 45
                fat = 0  # 50
                sodium = 0  # 1500
                calcium = 0  # 800
                iron = 0  # 15
                good_food_breakfast = []
                bad_food_breakfast = []

                for nut in nut_breakfast:
                    intake2['breakfast'][0] += nut.nutrition.energy * nut.portions
                    intake2['breakfast'][1] += nut.nutrition.carbohydrate * nut.portions
                    intake2['breakfast'][2] += nut.nutrition.protein * nut.portions
                    intake2['breakfast'][3] += nut.nutrition.fat * nut.portions
                    intake2['breakfast'][4] += nut.nutrition.sodium * 0.4 * nut.portions
                    intake2['breakfast'][5] += nut.nutrition.calcium * nut.portions
                    intake2['breakfast'][6] += nut.nutrition.iron * nut.portions
                    intake2['breakfast_per'][0] += nut.nutrition.energy * 100 / 2000 * nut.portions 
                    intake2['breakfast_per'][1] += nut.nutrition.carbohydrate * 100 / 300 * nut.portions
                    intake2['breakfast_per'][2] += nut.nutrition.protein * 100 / 45 * nut.portions
                    intake2['breakfast_per'][3] += nut.nutrition.fat * 100 / 50 * nut.portions
                    intake2['breakfast_per'][4] += nut.nutrition.sodium * 100 * 0.4 / 1500 * nut.portions
                    intake2['breakfast_per'][5] += nut.nutrition.calcium * 100 / 800 * nut.portions
                    intake2['breakfast_per'][6] += nut.nutrition.iron * 100 / 15 * nut.portions
                    energy += nut.nutrition.energy * nut.portions
                    carbohydrate += nut.nutrition.carbohydrate * nut.portions
                    protein += nut.nutrition.protein * nut.portions
                    fat += nut.nutrition.fat * nut.portions
                    sodium += nut.nutrition.sodium * nut.portions
                    calcium += nut.nutrition.calcium * nut.portions
                    iron += nut.nutrition.iron * nut.portions
                
                if 2000 * 0.2 <= energy and energy < 2000 * 0.4: good_food_breakfast.append('칼로리')
                else: bad_food_breakfast.append('칼로리')

                if 300 * 0.2 <= carbohydrate and carbohydrate < 300 * 0.4: good_food_breakfast.append('탄수화물')
                else: bad_food_breakfast.append('탄수화물')
                
                if 45 * 0.2 <= protein and protein < 45 * 0.4: good_food_breakfast.append('단백질')
                else: bad_food_breakfast.append('단백질')

                if 50 * 0.2 <= fat and fat < 50 * 0.4: good_food_breakfast.append('지방')
                else: bad_food_breakfast.append('지방')

                if 1500 * 0.4 * 0.2 <= sodium and sodium < 1500 * 0.4 * 0.4: good_food_breakfast.append('나트륨')
                else: bad_food_breakfast.append('나트륨')

                if 800 * 0.2 <= calcium and calcium < 800 * 0.4: good_food_breakfast.append('칼슘')
                else: bad_food_breakfast.append('칼슘')

                if 15 * 0.2 <= iron and iron < 15 * 0.4: good_food_breakfast.append('철분')
                else: bad_food_breakfast.append('철분')

                context['good_food_breakfast'] = good_food_breakfast
                context['bad_food_breakfast'] = bad_food_breakfast

            if nut_lunch:
                energy = 0  # 2000
                carbohydrate = 0  # 300
                protein = 0  # 45
                fat = 0  # 50
                sodium = 0  # 1500
                calcium = 0  # 800
                iron = 0  # 15
                good_food_lunch = []
                bad_food_lunch = []

                for nut in nut_lunch:
                    intake2['lunch'][0] += nut.nutrition.energy * nut.portions
                    intake2['lunch'][1] += nut.nutrition.carbohydrate * nut.portions
                    intake2['lunch'][2] += nut.nutrition.protein * nut.portions
                    intake2['lunch'][3] += nut.nutrition.fat * nut.portions
                    intake2['lunch'][4] += nut.nutrition.sodium * 0.4 * nut.portions
                    intake2['lunch'][5] += nut.nutrition.calcium * nut.portions
                    intake2['lunch'][6] += nut.nutrition.iron * nut.portions
                    intake2['lunch_per'][0] += nut.nutrition.energy * 100 / 2000 * nut.portions
                    intake2['lunch_per'][1] += nut.nutrition.carbohydrate * 100 / 300 * nut.portions
                    intake2['lunch_per'][2] += nut.nutrition.protein * 100 / 45 * nut.portions
                    intake2['lunch_per'][3] += nut.nutrition.fat * 100 / 50 * nut.portions
                    intake2['lunch_per'][4] += nut.nutrition.sodium * 100 * 0.4  / 1500 * nut.portions
                    intake2['lunch_per'][5] += nut.nutrition.calcium * 100 / 800 * nut.portions
                    intake2['lunch_per'][6] += nut.nutrition.iron * 100 / 15 * nut.portions
                    energy += nut.nutrition.energy * nut.portions
                    carbohydrate += nut.nutrition.carbohydrate * nut.portions
                    protein += nut.nutrition.protein * nut.portions
                    fat += nut.nutrition.fat * nut.portions
                    sodium += nut.nutrition.sodium * nut.portions
                    calcium += nut.nutrition.calcium * nut.portions
                    iron += nut.nutrition.iron * nut.portions
                
                if 2000 * 0.2 <= energy and energy < 2000 * 0.4: good_food_lunch.append('칼로리')
                else: bad_food_lunch.append('칼로리')

                if 300 * 0.2 <= carbohydrate and carbohydrate < 300 * 0.4: good_food_lunch.append('탄수화물')
                else: bad_food_lunch.append('탄수화물')
                
                if 45 * 0.2 <= protein and protein < 45 * 0.4: good_food_lunch.append('단백질')
                else: bad_food_lunch.append('단백질')

                if 50 * 0.2 <= fat and fat < 50 * 0.4: good_food_lunch.append('지방')
                else: bad_food_lunch.append('지방')

                if 1500 * 0.4 * 0.2 <= sodium and sodium < 1500 * 0.4 * 0.4: good_food_breakfast.append('나트륨')
                else: bad_food_lunch.append('나트륨')

                if 800 * 0.2 <= calcium and calcium < 800 * 0.4: good_food_lunch.append('칼슘')
                else: bad_food_lunch.append('칼슘')

                if 15 * 0.2 <= iron and iron < 15 * 0.4: good_food_lunch.append('철분')
                else: bad_food_lunch.append('철분')

                context['good_food_lunch'] = good_food_lunch
                context['bad_food_lunch'] = bad_food_lunch

            if nut_dinner:
                energy = 0  # 2000
                carbohydrate = 0  # 300
                protein = 0  # 45
                fat = 0  # 50
                sodium = 0  # 1500
                calcium = 0  # 800
                iron = 0  # 15
                good_food_dinner = []
                bad_food_dinner = []

                for nut in nut_dinner:
                    intake2['dinner'][0] += nut.nutrition.energy * nut.portions
                    intake2['dinner'][1] += nut.nutrition.carbohydrate * nut.portions
                    intake2['dinner'][2] += nut.nutrition.protein * nut.portions
                    intake2['dinner'][3] += nut.nutrition.fat * nut.portions
                    intake2['dinner'][4] += nut.nutrition.sodium * 0.4 * nut.portions
                    intake2['dinner'][5] += nut.nutrition.calcium * nut.portions
                    intake2['dinner'][6] += nut.nutrition.iron * nut.portions
                    intake2['dinner_per'][0] += nut.nutrition.energy * 100 / 2000 * nut.portions
                    intake2['dinner_per'][1] += nut.nutrition.carbohydrate * 100 / 300 * nut.portions
                    intake2['dinner_per'][2] += nut.nutrition.protein * 100 / 45 * nut.portions
                    intake2['dinner_per'][3] += nut.nutrition.fat * 100 / 50 * nut.portions
                    intake2['dinner_per'][4] += nut.nutrition.sodium * 100 * 0.4  / 1500 * nut.portions
                    intake2['dinner_per'][5] += nut.nutrition.calcium * 100 / 800 * nut.portions
                    intake2['dinner_per'][6] += nut.nutrition.iron * 100 / 15 * nut.portions
                    energy += nut.nutrition.energy * nut.portions
                    carbohydrate += nut.nutrition.carbohydrate * nut.portions
                    protein += nut.nutrition.protein * nut.portions
                    fat += nut.nutrition.fat * nut.portions
                    sodium += nut.nutrition.sodium * nut.portions
                    calcium += nut.nutrition.calcium * nut.portions
                    iron += nut.nutrition.iron * nut.portions
                
                if 2000 * 0.2 <= energy and energy < 2000 * 0.4: good_food_dinner.append('칼로리')
                else: bad_food_dinner.append('칼로리')

                if 300 * 0.2 <= carbohydrate and carbohydrate < 300 * 0.4: good_food_dinner.append('탄수화물')
                else: bad_food_dinner.append('탄수화물')
                
                if 45 * 0.2 <= protein and protein < 45 * 0.4: good_food_dinner.append('단백질')
                else: bad_food_dinner.append('단백질')

                if 50 * 0.2 <= fat and fat < 50 * 0.4: good_food_dinner.append('지방')
                else: bad_food_dinner.append('지방')

                if 1500 * 0.4 * 0.2 <= sodium and sodium < 1500 * 0.4 * 0.4: good_food_breakfast.append('나트륨')
                else: bad_food_dinner.append('나트륨')

                if 800 * 0.2 <= calcium and calcium < 800 * 0.4: good_food_dinner.append('칼슘')
                else: bad_food_dinner.append('칼슘')

                if 15 * 0.2 <= iron and iron < 15 * 0.4: good_food_dinner.append('철분')
                else: bad_food_dinner.append('철분')

                context['good_food_dinner'] = good_food_dinner
                context['bad_food_dinner'] = bad_food_dinner

            j_intake = json.dumps(intake2)

            context['intake'] = j_intake
            context['kid'] = kid

            if morning_meal or lunch_meal or evening_meal:
                return render(request, 'meal/meal.html', context=context)
            else:
                return render(request, 'meal/meal.html', context=context)
        except: pass
        return render(request, 'meal/meal.html', context=context)

    # 날짜 선택할 경우
    if request.method == "POST":
        kid_id = request.POST.get('kid_id')
        context['kid_id'] = kid_id
        kid = Kid.objects.get(id=kid_id)
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

            nut_breakfast = 0
            nut_lunch = 0
            nut_dinner = 0
            try: nut_breakfast = Diet.objects.filter(meal__regdate=date) & Diet.objects.filter(meal__kid=kid) & Diet.objects.filter(meal__time='아침')
            except: pass
            try: nut_lunch = Diet.objects.filter(meal__regdate=date) & Diet.objects.filter(meal__kid=kid) & Diet.objects.filter(meal__time='점심')
            except: pass
            try: nut_dinner = Diet.objects.filter(meal__regdate=date) & Diet.objects.filter(meal__kid=kid) & Diet.objects.filter(meal__time='저녁')
            except: pass

            intake2 = {}
            intake2['breakfast'] = [0]*7
            intake2['lunch'] = [0]*7
            intake2['dinner'] = [0]*7
            intake2['breakfast_per'] = [0]*7
            intake2['lunch_per'] = [0]*7
            intake2['dinner_per'] = [0]*7

            if nut_breakfast:
                energy = 0  # 2000
                carbohydrate = 0  # 300
                protein = 0  # 45
                fat = 0  # 50
                sodium = 0  # 1500
                calcium = 0  # 800
                iron = 0  # 15
                good_food_breakfast = []
                bad_food_breakfast = []

                for nut in nut_breakfast:
                    intake2['breakfast'][0] += nut.nutrition.energy * nut.portions
                    intake2['breakfast'][1] += nut.nutrition.carbohydrate * nut.portions
                    intake2['breakfast'][2] += nut.nutrition.protein * nut.portions
                    intake2['breakfast'][3] += nut.nutrition.fat * nut.portions
                    intake2['breakfast'][4] += nut.nutrition.sodium * 0.4 * nut.portions
                    intake2['breakfast'][5] += nut.nutrition.calcium * nut.portions
                    intake2['breakfast'][6] += nut.nutrition.iron * nut.portions
                    intake2['breakfast_per'][0] += nut.nutrition.energy * 100 / 2000 * nut.portions
                    intake2['breakfast_per'][1] += nut.nutrition.carbohydrate * 100 / 300 * nut.portions
                    intake2['breakfast_per'][2] += nut.nutrition.protein * 100 / 45 * nut.portions
                    intake2['breakfast_per'][3] += nut.nutrition.fat * 100 / 50 * nut.portions
                    intake2['breakfast_per'][4] += nut.nutrition.sodium * 100 * 0.4 / 1500 * nut.portions
                    intake2['breakfast_per'][5] += nut.nutrition.calcium * 100 / 800 * nut.portions
                    intake2['breakfast_per'][6] += nut.nutrition.iron * 100 / 15 * nut.portions
                    energy += nut.nutrition.energy * nut.portions
                    carbohydrate += nut.nutrition.carbohydrate * nut.portions
                    protein += nut.nutrition.protein * nut.portions
                    fat += nut.nutrition.fat * nut.portions
                    sodium += nut.nutrition.sodium * nut.portions
                    calcium += nut.nutrition.calcium * nut.portions
                    iron += nut.nutrition.iron * nut.portions
                
                if 2000 * 0.2 <= energy and energy < 2000 * 0.4: good_food_breakfast.append('칼로리')
                else: bad_food_breakfast.append('칼로리')

                if 300 * 0.2 <= carbohydrate and carbohydrate < 300 * 0.4: good_food_breakfast.append('탄수화물')
                else: bad_food_breakfast.append('탄수화물')
                
                if 45 * 0.2 <= protein and protein < 45 * 0.4: good_food_breakfast.append('단백질')
                else: bad_food_breakfast.append('단백질')

                if 50 * 0.2 <= fat and fat < 50 * 0.4: good_food_breakfast.append('지방')
                else: bad_food_breakfast.append('지방')

                if 1500 * 0.4 * 0.2 <= sodium and sodium < 1500 * 0.4 * 0.4: good_food_breakfast.append('나트륨')
                else: bad_food_breakfast.append('나트륨')

                if 800 * 0.2 <= calcium and calcium < 800 * 0.4: good_food_breakfast.append('칼슘')
                else: bad_food_breakfast.append('칼슘')

                if 15 * 0.2 <= iron and iron < 15 * 0.4: good_food_breakfast.append('철분')
                else: bad_food_breakfast.append('철분')

                context['good_food_breakfast'] = good_food_breakfast
                context['bad_food_breakfast'] = bad_food_breakfast

            if nut_lunch:
                energy = 0  # 2000
                carbohydrate = 0  # 300
                protein = 0  # 45
                fat = 0  # 50
                sodium = 0  # 1500
                calcium = 0  # 800
                iron = 0  # 15
                good_food_lunch = []
                bad_food_lunch = []

                for nut in nut_lunch:
                    intake2['lunch'][0] += nut.nutrition.energy * nut.portions
                    intake2['lunch'][1] += nut.nutrition.carbohydrate * nut.portions
                    intake2['lunch'][2] += nut.nutrition.protein * nut.portions
                    intake2['lunch'][3] += nut.nutrition.fat * nut.portions
                    intake2['lunch'][4] += nut.nutrition.sodium * 0.4  * nut.portions
                    intake2['lunch'][5] += nut.nutrition.calcium * nut.portions
                    intake2['lunch'][6] += nut.nutrition.iron * nut.portions
                    intake2['lunch_per'][0] += nut.nutrition.energy * 100 / 2000 * nut.portions
                    intake2['lunch_per'][1] += nut.nutrition.carbohydrate * 100 / 300 * nut.portions
                    intake2['lunch_per'][2] += nut.nutrition.protein * 100 / 45 * nut.portions
                    intake2['lunch_per'][3] += nut.nutrition.fat * 100 / 50 * nut.portions
                    intake2['lunch_per'][4] += nut.nutrition.sodium * 100 * 0.4  / 1500 * nut.portions
                    intake2['lunch_per'][5] += nut.nutrition.calcium * 100 / 800 * nut.portions
                    intake2['lunch_per'][6] += nut.nutrition.iron * 100 / 15 * nut.portions
                    energy += nut.nutrition.energy * nut.portions
                    carbohydrate += nut.nutrition.carbohydrate * nut.portions
                    protein += nut.nutrition.protein * nut.portions
                    fat += nut.nutrition.fat * nut.portions
                    sodium += nut.nutrition.sodium * nut.portions
                    calcium += nut.nutrition.calcium * nut.portions
                    iron += nut.nutrition.iron * nut.portions
                energy_result = '칼로리(' + str(round(energy, 2)) + '/2000)'
                print(energy_result)
                if 2000 * 0.2 <= energy and energy < 2000 * 0.4: good_food_lunch.append(energy_result)
                else: bad_food_lunch.append(energy_result)

                if 300 * 0.2 <= carbohydrate and carbohydrate < 300 * 0.4: good_food_lunch.append('탄수화물')
                else: bad_food_lunch.append('탄수화물')
                
                if 45 * 0.2 <= protein and protein < 45 * 0.4: good_food_lunch.append('단백질')
                else: bad_food_lunch.append('단백질')

                if 50 * 0.2 <= fat and fat < 50 * 0.4: good_food_lunch.append('지방')
                else: bad_food_lunch.append('지방')

                if 1500 * 0.4 * 0.2 <= sodium and sodium < 1500 * 0.4 * 0.4: good_food_breakfast.append('나트륨')
                else: bad_food_lunch.append('나트륨')

                if 800 * 0.2 <= calcium and calcium < 800 * 0.4: good_food_lunch.append('칼슘')
                else: bad_food_lunch.append('칼슘')

                if 15 * 0.2 <= iron and iron < 15 * 0.4: good_food_lunch.append('철분')
                else: bad_food_lunch.append('철분')

                context['good_food_lunch'] = good_food_lunch
                context['bad_food_lunch'] = bad_food_lunch

            if nut_dinner:
                energy = 0  # 2000
                carbohydrate = 0  # 300
                protein = 0  # 45
                fat = 0  # 50
                sodium = 0  # 1500
                calcium = 0  # 800
                iron = 0  # 15
                good_food_dinner = []
                bad_food_dinner = []

                for nut in nut_dinner:
                    intake2['dinner'][0] += nut.nutrition.energy * nut.portions
                    intake2['dinner'][1] += nut.nutrition.carbohydrate * nut.portions
                    intake2['dinner'][2] += nut.nutrition.protein * nut.portions
                    intake2['dinner'][3] += nut.nutrition.fat * nut.portions
                    intake2['dinner'][4] += nut.nutrition.sodium * 0.4 * nut.portions
                    intake2['dinner'][5] += nut.nutrition.calcium * nut.portions
                    intake2['dinner'][6] += nut.nutrition.iron * nut.portions
                    intake2['dinner_per'][0] += nut.nutrition.energy * 100 / 2000 * nut.portions
                    intake2['dinner_per'][1] += nut.nutrition.carbohydrate * 100 / 300 * nut.portions
                    intake2['dinner_per'][2] += nut.nutrition.protein * 100 / 45 * nut.portions
                    intake2['dinner_per'][3] += nut.nutrition.fat * 100 / 50 * nut.portions
                    intake2['dinner_per'][4] += nut.nutrition.sodium * 100 * 0.4  / 1500 * nut.portions
                    intake2['dinner_per'][5] += nut.nutrition.calcium * 100 / 800 * nut.portions
                    intake2['dinner_per'][6] += nut.nutrition.iron * 100 / 15 * nut.portions
                    energy += nut.nutrition.energy * nut.portions
                    carbohydrate += nut.nutrition.carbohydrate * nut.portions
                    protein += nut.nutrition.protein * nut.portions
                    fat += nut.nutrition.fat * nut.portions
                    sodium += nut.nutrition.sodium * nut.portions
                    calcium += nut.nutrition.calcium * nut.portions
                    iron += nut.nutrition.iron * nut.portions
                
                if 2000 * 0.2 <= energy and energy < 2000 * 0.4: good_food_dinner.append('칼로리')
                else: bad_food_dinner.append('칼로리')

                if 300 * 0.2 <= carbohydrate and carbohydrate < 300 * 0.4: good_food_dinner.append('탄수화물')
                else: bad_food_dinner.append('탄수화물')
                
                if 45 * 0.2 <= protein and protein < 45 * 0.4: good_food_dinner.append('단백질')
                else: bad_food_dinner.append('단백질')

                if 50 * 0.2 <= fat and fat < 50 * 0.4: good_food_dinner.append('지방')
                else: bad_food_dinner.append('지방')

                if 1500 * 0.4 * 0.2 <= sodium and sodium < 1500 * 0.4 * 0.4: good_food_breakfast.append('나트륨')
                else: bad_food_dinner.append('나트륨')

                if 800 * 0.2 <= calcium and calcium < 800 * 0.4: good_food_dinner.append('칼슘')
                else: bad_food_dinner.append('칼슘')

                if 15 * 0.2 <= iron and iron < 15 * 0.4: good_food_dinner.append('철분')
                else: bad_food_dinner.append('철분')

                print('value:', energy, '%:', energy * 100 / 2000, 'start', 2000 * 0.2, 'end', 2000 * 0.4)
                print('value:', carbohydrate, '%:', carbohydrate * 100 / 300, 'start', 300 * 0.2, 'end', 300 * 0.4)
                print('value:', protein, '%:', protein * 100 / 45, 'start', 45 * 0.2, 'end', 45 * 0.4)
                print('value:', fat, '%:', fat * 100 / 50, 'start', 50 * 0.2, 'end', 50 * 0.4)
                print('value:', sodium, '%:', sodium * 0.4 * 100 / 1500, 'start', 1500 * 0.2, 'end', 1500 * 0.4)
                print('value:', calcium, '%:', calcium * 100 / 800, 'start', 800 * 0.2, 'end', 800 * 0.4)
                print('value:', iron, '%:', iron * 100 / 15, 'start', 15 * 0.2, 'end', 15 * 0.4)

                context['good_food_dinner'] = good_food_dinner
                context['bad_food_dinner'] = bad_food_dinner

            j_intake = json.dumps(intake2)

            context['intake'] = j_intake
            context['kid'] = kid

            if morning_meal or lunch_meal or evening_meal:
                return render(request, 'meal/meal.html', context=context)
            else:
                return render(request, 'meal/meal.html', context=context)
        except: pass
        return render(request, 'meal/meal.html', context=context)

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
    kid_id = request.POST['kid_id']
    try: kid = Kid.objects.get(id=kid_id)
    except: pass

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

    kid_id = req['kid_id']
    kid = Kid.objects.get(id=kid_id)

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
