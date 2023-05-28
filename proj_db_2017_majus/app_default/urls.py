from django.urls import path
from .views import index, feltoltes, feladat2 #, feladat3, feladat4, feladat5

urlpatterns = [
    path('', index),
    path('feltoltes/<str:table>', feltoltes),
    path('feladat/2', feladat2),
]