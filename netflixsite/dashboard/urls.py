# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage'),
    path('genres_plot/', views.genre_plot, name='genre_plot'),
    path('search/', views.search, name='search'),
]
