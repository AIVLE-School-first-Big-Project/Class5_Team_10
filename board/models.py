from django.db import models
# from django.contrib.auth.models import User
from user.models import User

# Create your models here.
class Board(models.Model):
    board_id = models.AutoField(primary_key=True, null=False)
    board_name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.board_name

class Post(models.Model):
    post_id = models.AutoField(primary_key=True, null=False)
    post_title = models.CharField(max_length=20, null=False)
    post_content = models.TextField(null=False)
    post_img = models.ImageField(null=False)
    post_regdate = models.DateField(null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 관리자만 사용
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_title

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, null=False)
    comment_content = models.TextField(null=False)
    comment_regdate = models.DateField(null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_content