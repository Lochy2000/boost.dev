from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Removed index path since the view doesn't exist
    path('community/', views.community, name='community'),
    path('tech_news/', views.tech_news, name='tech_news'),
]