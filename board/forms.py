from django import forms
from board.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # 사용할 모델
        fields = ['title', 'content', 'board']
        labels = {
            'title' : '제목',
            'content' : '내용',
            'board' : '카테고리',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }