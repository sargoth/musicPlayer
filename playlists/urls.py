from django.urls import path, include
from playlists import views

app_name = "playlists"

urlpatterns = [
    path('playlists/', include([
        path('', views.PlaylistListView.as_view(), name="list_playlists"),
        path('create/', views.PlaylistCreateView.as_view(), name="create_playlist"),
        path('<int:pk>/', include([
            path('', views.PlaylistDetailView.as_view(), name="playlist_detail"),
            path('delete/', views.PlaylistDeleteView.as_view(), name="delete_playlist"),
            path('edit/', views.PlaylistEditView.as_view(), name="edit_playlist"),
        ])),
        path('<int:playlist_pk>/remove_track/<int:track_pk>/', views.RemoveTrackFromPlaylistView.as_view(), name="remove_track")
    ]))
]
