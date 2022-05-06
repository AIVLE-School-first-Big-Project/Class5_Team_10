from django.db import models
from user.models import Kid


# Create your models here.
def user_directory_path(instance, filename):
    return 'meal_images/kid_{}/{}_{}{}'.format(
        instance.kid.id, instance.regdate, instance.time, '.png')


class Meal(models.Model):  # 식사
    id = models.AutoField(primary_key=True, null=False)
    img = models.ImageField(null=True, upload_to=user_directory_path)
    regdate = models.DateField(null=False)
    time = models.CharField(max_length=20, null=False)
    kid = models.ForeignKey(Kid, on_delete=models.CASCADE)


class Nutrition(models.Model):  # 영양성분
    id = models.AutoField(primary_key=True, null=False)
    food = models.CharField(max_length=30, null=False)
    quantity = models.FloatField(null=True)  # 중량(g)
    energy = models.FloatField(null=True)  # 에너지(kcal)
    carbohydrate = models.FloatField(null=True)  # 탄수화물(g)
    sugars = models.FloatField(null=True)  # 당류(g)
    fat = models.FloatField(null=True)  # 지방(g)
    protein = models.FloatField(null=True)  # 단백질(g)
    calcium = models.FloatField(null=True)  # 칼슘(mg)
    phosphorus = models.FloatField(null=True)  # 인(mg)
    sodium = models.FloatField(null=True)  # 나트륨(mg)
    potassium = models.FloatField(null=True)  # 칼륨(mg)
    magnesium = models.FloatField(null=True)  # 마그네슘(mg)
    iron = models.FloatField(null=True)  # 철분(mg)
    zinc = models.FloatField(null=True)  # 아연(mg)
    cholesterol = models.FloatField(null=True)  # 콜레스테롤(mg)
    transfat = models.FloatField(null=True)  # 트랜스지방(g)

    # csv 파일 db저장
    def __str__(self):
        return '{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
            self.food,
            self.quantity,
            self.energy,
            self.carbohydrate,
            self.sugars,
            self.fat,
            self.protein,
            self.calcium,
            self.phosphorus,
            self.sodium,
            self.potassium,
            self.magnesium,
            self.iron,
            self.zinc,
            self.cholesterol,
            self.transfat)


class Diet(models.Model):  # 식단
    id = models.AutoField(primary_key=True, null=False)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    portions = models.FloatField(default=1, null=False)
    nutrition = models.ForeignKey(Nutrition, on_delete=models.DO_NOTHING)
