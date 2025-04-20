from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index'),
    path('community/', views.community, name='community'),
]