# wins/urls.py
from django.urls import path
from . import views

app_name = 'wins'

urlpatterns = [
    path('submit/', views.submit_win, name='submit_win'),
    path('view/<int:win_id>/', views.view_win, name='view_win'),
    path('my-wins/', views.my_wins, name='my_wins'),
    path('community/', views.community_wins, name='community_wins'),
    path('toggle-public/<int:win_id>/', views.toggle_public, name='toggle_public'),
    path('celebrate/<int:win_id>/', views.toggle_celebration, name='toggle_celebration'),
]