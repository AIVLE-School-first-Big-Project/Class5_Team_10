from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager
# Create your models here.
# class User(models.Model):
# 	name = models.CharField(max_length=255)
# 	class Meta:	

# 		# 데이터 조회 기본 정렬 상태
# 		ordering = ['-id', 'name']


# 커스텀 유저만듦 -> AbstractBaseUser 이거를 상속받아서 만들면 그게 유저필드가 됨
# 장고에서 기본으로 제공하는 auth_user 안쓰고 커스텀한거 쓰려면 settings 가서 AUTH_USER_MODEL = '내가만든이름.User' 적어줘야함
# TextField는 길이 제한없음, CharField는 길이제한을 써줘야함
class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True, null=False)
    id = models.CharField(max_length=20, unique=True, null=False)
    name = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=15, null=False)
# 실제로 유저를 선택하면 그 유저의 이름을 어떤필드를 쓸거냐
    USERNAME_FIELD = 'id'
    objects = UserManager()
# Meta 안해주면 user_user 테이블이 됨
    class Meta:
        db_table = "User"

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, id, name, email, password):
        if not id :
            raise ValueError('must have user id')
        if not name:
            raise ValueError('must have user name')
        if not email:
            raise ValueError('must have user email')
        if not password:
            raise ValueError('must have user password')

        user = self.model(
            id = id,
            name = name,
            email = email
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

class Kid(models.Model):
    kid_id = models.AutoField(primary_key=True, null=False)
    kid_name = models.CharField(max_length=20, null=False)
    birthday = models.DateField(null=False)
    kid_img = models.ImageField(null=False)
    kid_height = models.FloatField(null=False)
    kid_weight = models.FloatField(null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.kid_name