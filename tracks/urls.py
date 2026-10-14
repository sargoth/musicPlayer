from django.urls import path, include

from tracks import views

app_name = 'tracks'

urlpatterns = [
    path('tracks/', include([
        path('create/', views.TrackCreateView.as_view(), name='create_track'),
        path('<int:pk>/delete/', views.TrackDeleteView.as_view(), name='delete_track')
    ]))
]
