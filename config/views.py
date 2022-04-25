from django.shortcuts import render, redirect, get_object_or_404

def main(request):
    return render(request, 'main.html')