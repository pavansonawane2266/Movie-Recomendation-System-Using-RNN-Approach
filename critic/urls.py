from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = 'critic-index'),
    path('movies', views.movies, name='critic-movies'),
    path('review/<int:pk>', views.review, name='critic-review'),
]
