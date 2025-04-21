from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenge_list, name='challenges'),
    path('new/', views.create_challenge, name='new_challenge'),
    path('<int:pk>/', views.challenge_detail, name='challenge_detail'),
    path('<int:pk>/submit/', views.submit_solution, name='submit_solution'),
    path('generate/', views.generate_ai_challenge, name='generate_challenge'),
    path('quotes/', views.quote_list, name='quotes'),  # Temporary until quotes are moved
]