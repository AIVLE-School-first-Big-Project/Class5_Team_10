from django.db import models
from user.models import User
from datetime import datetime


def board_dir_path(instance, filename):
    ctg = instance.board.ctg
    time = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    return 'board_images/{}/{}_{}'.format(ctg, time, '.png')


class Board(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    ctg = models.CharField(max_length=20, null=False)  # 카테고리

    class Meta:
        unique_together = ['ctg']

    def __str__(self):
        return self.ctg


class Post(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=20, null=False)
    content = models.TextField(null=False)
    img = models.ImageField(null=True, blank=True, upload_to=board_dir_path)
    regdate = models.DateTimeField(null=False)
    moddate = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 관리자만 사용
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    content = models.TextField(null=False)
    regdate = models.DateTimeField(null=False)
    moddate = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
