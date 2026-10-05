from django.urls import path, include

from tracks import views

app_name = 'tracks'

urlpatterns = [
    path('tracks/', include([
        path('create/', views.create_track_view, name='create_track'),
        path('<int:pk>/delete/', views.delete_track_view, name='delete_track')
    ]))
]
