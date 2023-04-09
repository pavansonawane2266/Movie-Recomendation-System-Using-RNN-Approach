from os import name
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='admin-index'),
    path('train-dataset', views.train_dataset, name='admin-train-dataset'),
    path('test-dataset', views.test_model, name='admin-test-dataset'),
    path('critics', views.critics, name='admin-critics'),
    path('critics-activate/<int:pk>', views.criticsActivate, name='admin-critics-active'),
    path('critics-inactivate/<int:pk>', views.criticsInactive, name='admin-critics-inactive'),
]
