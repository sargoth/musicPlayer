from django.urls import path, include

from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('artists/', include([
        path('', views.list_all_artists_view, name='list_artists'),
        path('<int:pk>/', views.artist_details_view, name='artist_detail')
    ])),
    path('albums/', include([
        path('', views.list_all_albums_view, name='list_albums'),
        path('create/', views.create_album_view, name='create_album'),
        path('<int:pk>/', views.album_details_view, name='album-detail'),
        path('<int:pk>/delete/', views.delete_album_view, name='delete-album')
    ])),
]
