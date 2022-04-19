from django.contrib import admin
from .models import Meal, Nutrition, Diet

# Register your models here.
admin.site.register(Meal)
admin.site.register(Nutrition)
admin.site.register(Diet)