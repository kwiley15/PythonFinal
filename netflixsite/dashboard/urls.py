# dashboard/urls.py
from django.urls import path
from . import views

# Define URL patterns for the dashboard app
urlpatterns = [
    path('', views.index, name='index'),  # Homepage'),
    path('genres_plot/', views.genre_plot, name='genre_plot'), # returns and generates visualizations for genres
    path('search/', views.search, name='search'), # search page for searching the neflix titles 

]

