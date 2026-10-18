from django.urls import path, include

from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('artists/', include([
        path('', views.ArtistListView.as_view(), name='list_artists'),
        path('create/', views.ArtistCreateView.as_view(), name='create_artist'),
        path('<int:pk>/', views.ArtistDetailsView.as_view(), name='artist_detail'),
        path('<int:pk>/delete/', views.ArtistDeleteView.as_view(), name='delete_artist'),
        path('<int:pk>/edit/', views.ArtistUpdateView.as_view(), name='edit_artist')
    ])),
    path('albums/', include([
        path('', views.AlbumListView.as_view(), name='list_albums'),
        path('create/', views.AlbumCreateView.as_view(), name='create_album'),
        path('<int:pk>/', views.AlbumDetailsView.as_view(), name='album_detail'),
        path('<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='delete_album'),
        path('<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='edit_album')
    ])),
    path('genres/', include([
        path('', views.GenreListView.as_view(), name='list_genres'),
        path('create/', views.GenreCreateView.as_view(), name='create_genre'),
        path('<int:pk>/', include([
            path('edit/', views.GenreUpdateView.as_view(), name='edit_genre'),
            path('delete/', views.GenreDeleteView.as_view(), name='delete_genre')
        ]))
    ])),
    path('search/', views.SearchView.as_view(), name="search")
]
