from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'board'

urlpatterns = [
    path('',  views.post_list, name='post_list'),
    path('<int:post_id>/',  views.post, name='post'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/delete/<int:post_id>', views.post_delete, name='post_delete')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
