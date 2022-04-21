from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User, Kid


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("id", "password1", "password2" , "name", "email" )


class KidRegisterForm(forms.ModelForm):

    class Meta:
        model = Kid
        fields = ("name", "birthday", "img", "height", "weight")