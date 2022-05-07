from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'board'

urlpatterns = [
    path('',  views.post_list, name='post_list'),
    path('<int:post_id>/',  views.post, name='post'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/modify/<int:post_id>', views.post_modify, name='post_modify'),
    path('post/delete/<int:post_id>', views.post_delete, name='post_delete'),
    path('post/comment/modify/<int:comment_id>',
         views.comment_modify, name='comment_modify'),
    path('post/comment/delete/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
