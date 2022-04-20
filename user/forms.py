from django.contrib.auth.forms import UserCreationForm
from user.models import User


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("id", "password1", "password2" , "name", "email" )
