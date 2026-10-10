from django.contrib import admin
from django.urls import path, include

from musicPlayer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('', include('catalog.urls')),
    path('', include('tracks.urls')),
    path('', include('playlists.urls'))
]
