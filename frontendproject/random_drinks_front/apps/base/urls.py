from django.urls import path
from frontendproject.random_drinks_front.apps.base import views

urlpatterns = [

    path('', views.index, name='index'),

]