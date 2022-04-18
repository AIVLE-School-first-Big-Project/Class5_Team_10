from django.db import models
from user.models import Kid

# Create your models here.
class Meal(models.Model):  # 식사
    meal_id = models.AutoField(primary_key=True, null=False)
    meal_img = models.ImageField()
    meal_regdate = models.DateField(null=False)
    meal_time = models.CharField(max_length=20, null=False)
    kid_id = models.ForeignKey(Kid, on_delete=models.CASCADE)

class Nutrition(models.Model):  # 영양성분
    nutrition_id = models.AutoField(primary_key=True, null=False)
    food_name = models.CharField(max_length=30, null=False)
    quantity = models.FloatField(null=False)  # 중량(g)
    energy = models.FloatField(null=False)  # 에너지(kcal)
    carbohydrate = models.FloatField(null=False)  # 탄수화물(g)
    sugars = models.FloatField(null=False)  # 당류(g)
    fat = models.FloatField(null=False)  # 지방(g)
    protein = models.FloatField(null=False)  # 단백질(g)
    calcium = models.FloatField(null=False)  # 칼슘(mg)
    phosphorus = models.FloatField(null=False)  # 인(mg)
    sodium = models.FloatField(null=False)  # 나트륨(mg)
    iron = models.FloatField(null=False)  # 철분(mg)
    zinc = models.FloatField(null=False)  # 아연(mg)
    cholesterol = models.FloatField(null=False)  # 콜레스테롤(mg)
    transfat = models.FloatField(null=False)  # 트랜스지방(g)

    def __str__(self):
        return self.food_name

class Diet(models.Model):  # 식단
    diet_id = models.AutoField(primary_key=True, null=False)
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    nutrition_id = models.ForeignKey(Nutrition, on_delete=models.DO_NOTHING)