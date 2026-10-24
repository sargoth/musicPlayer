from django.urls import path, include

from tracks import views

app_name = 'tracks'

urlpatterns = [
    path('tracks/', include([
        path('create/', views.TrackCreateView.as_view(), name='create_track'),
        path('<int:pk>/', include([
            path('delete/', views.TrackDeleteView.as_view(), name='delete_track'),
            path('play/', views.track_times_played_view, name='track_times_played'),
            path("seek/", views.TrackSeekView.as_view(), name="track_seek")
        ]))
    ]))
]
