from django.conf import settings
from django.conf.urls.static import static
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

handler404 = "django.views.defaults.page_not_found"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
