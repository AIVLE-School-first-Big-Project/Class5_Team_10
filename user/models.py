from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators

class User(AbstractUser):
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
    img = models.ImageField(null=False)
    height = models.FloatField(null=False)
    weight = models.FloatField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name