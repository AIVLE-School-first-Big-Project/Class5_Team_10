from django.db import models
from user.models import Kid

# Create your models here.
def user_directory_path(instance, filename):
    return 'meal_images/kid_{}/{}_{}{}'.format(instance.kid.id, instance.regdate, instance.time, '.png')

class Meal(models.Model):  # 식사
    id = models.AutoField(primary_key=True, null=False)
    img = models.ImageField(null=True, upload_to=user_directory_path)
    regdate = models.DateField(null=False)
    time = models.CharField(max_length=20, null=False)
    kid = models.ForeignKey(Kid, on_delete=models.CASCADE)

class Nutrition(models.Model):  # 영양성분
    id = models.AutoField(primary_key=True, null=False)
    food = models.CharField(max_length=30, null=False)
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
        return self.food

class Diet(models.Model):  # 식단
    id = models.AutoField(primary_key=True, null=False)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    nutrition = models.ForeignKey(Nutrition, on_delete=models.DO_NOTHING)