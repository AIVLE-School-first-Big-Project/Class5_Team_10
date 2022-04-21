from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meal/', include('meal.urls')),
    path('board/', include('board.urls')),
    path('user/', include('user.urls'))
]
