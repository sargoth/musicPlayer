from django.urls import path, include
from playlists import views

app_name = "playlists"

urlpatterns = [
    path('playlists/', include([
        path('', views.PlaylistListView.as_view(), name="list_playlists"),
        path('<int:pk>/', views.PlaylistDetailView.as_view(), name="playlist_detail"),
    ])),
    path('create/', views.PlaylistCreateView.as_view(), name="create_playlist"),
    path('<int:playlist_pk>/remove_track/<int:track_pk>/', views.RemoveTrackFromPlaylistView.as_view(), name="remove_track")
]