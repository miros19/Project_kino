from django.urls import path

from .views import *

app_name = 'movies'

#Urls used to work with movies and tickets
urlpatterns = [
   path('all', show_all_movies, name = 'all_movies'),
   path('my', show_my_movies, name = 'my_movies'),
   path('details', show_movie_details, name = 'movie_details'),
   path('buy', buy_movie, name = 'buy_movie')
]