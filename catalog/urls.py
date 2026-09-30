from django.urls import path

from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('artists/', views.list_all_artists_view, name='list_artists'),
    path('artists/<int:pk>', views.artist_details_view, name='artist_detail'),
    path('albums/', views.list_all_albums_view, name='list_albums'),
    path('albums/<int:pk>', views.album_details_view, name='album-detail')
]
