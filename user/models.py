from email.policy import default
from tokenize import blank_re
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from datetime import datetime



def user_directory_path(instance, filename):
    return 'kid_images/{}_{}_{}'.format(instance.name, datetime.today().strftime('%Y-%m-%d-%H-%M-%S'), filename)

class User(AbstractUser):
    # username = None
    first_name = None
    last_name = None
    user_id = models.AutoField(primary_key=True, null=False)
    id = models.CharField(_('id'), max_length=20, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid id. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that id already exists."),
        })
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
    img = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    height = models.FloatField(null=False)
    weight = models.FloatField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_img(self):
        # variable PATH_TO_DEFAULT_STATIC_IMAGE depends on the enviroment
        # on development, it would be something like "localhost:8000/static/default_avatar.png"
        # on production, it would be something like "https://BUCKET_NAME.s3.amazonaws.com/static/default_avatar.png"
        return self.img if self.img else 'http://127.0.0.1:8000/user/static/images/kid_profile_default.PNG'    

