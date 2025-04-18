from django.urls import path
from . import views

urlpatterns = [
    path('', views.submission_list, name='submissions'),
    path('new/', views.new_submission, name='new_submission'),
]