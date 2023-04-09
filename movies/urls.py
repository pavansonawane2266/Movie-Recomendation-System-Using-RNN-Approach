from os import name
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='admin-movies-index'),
    path('create', views.create, name='admin-movies-create'),
]
