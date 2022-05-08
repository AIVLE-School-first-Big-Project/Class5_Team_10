from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('admin/', admin.site.urls),
    path('meal/', include('meal.urls')),
    path('board/', include('board.urls')),
    path('user/', include('user.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^media/(?P<path>.*)$',
            serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'config.views.page_not_found'
handler500 = 'config.views.server_error'
