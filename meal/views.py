from django.shortcuts import render, redirect

# Create your views here.
def meal(request):
    return render(request, 'meal/meal.html')