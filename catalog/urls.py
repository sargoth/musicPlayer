from django.urls import path, include

from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('artists/', include([
        path('', views.list_all_artists_view, name='list_artists'),
        path('create/', views.create_artist_view, name='create_artist'),
        path('<int:pk>/', views.artist_details_view, name='artist_detail'),
        path('<int:pk>/delete/', views.delete_artist_view, name='delete_artist'),
        path('<int:pk>/edit/', views.edit_artist_view, name='edit_artist')
    ])),
    path('albums/', include([
        path('', views.list_all_albums_view, name='list_albums'),
        path('create/', views.create_album_view, name='create_album'),
        path('<int:pk>/', views.album_details_view, name='album_detail'),
        path('<int:pk>/delete/', views.delete_album_view, name='delete_album'),
        path('<int:pk>/edit/', views.edit_album_view, name='edit_album')
    ])),
]
