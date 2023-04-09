from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('reviews/<int:pk>', views.reviews, name='reviews-index'),
]
