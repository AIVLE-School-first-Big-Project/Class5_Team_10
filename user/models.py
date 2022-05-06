from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime


def user_directory_path(instance, filename):
    return 'kid_images/{}_{}_{}'.format(instance.name,
                                        datetime.today()
                                        .strftime('%Y-%m-%d-%H-%M-%S'),
                                        filename)


class User(AbstractUser):
    first_name = None
    last_name = None
    user_id = models.AutoField(primary_key=True, null=False)
    id = models.CharField(_('id'), max_length=20, unique=True)
    name = models.CharField(_('name'), max_length=20, blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = "User"

    def __str__(self):
        return self.name


class Kid(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=20, null=False)
    birthday = models.DateField(null=False)
    img = models.ImageField(upload_to=user_directory_path,
                            blank=True, null=True)
    height = models.FloatField(null=False)
    weight = models.FloatField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_img(self):
        return self.img if self.img else\
            'http://127.0.0.1:8000/user/static/images/kid_profile_default.PNG'
