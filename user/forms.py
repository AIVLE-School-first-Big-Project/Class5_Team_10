from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User, Kid


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("id", "password1", "password2", "name", "email")


class KidRegisterForm(forms.ModelForm):
    class Meta:
        model = Kid
        fields = ("name", "birthday", "img", "height", "weight")


class UpdateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("password1", "password2", "email")


class UpdateKidForm(forms.ModelForm):

    class Meta:
        model = Kid
        fields = ("img", "height", "weight")
