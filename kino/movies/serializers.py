from rest_framework import serializers

from .models import *

#Serializer used to manage basic movie data
class BasicMovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ['id','title', 'price']

#Serializer used to manage movie details
class DetailMovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ['id','title', 'price', 'rating', 'description']

#Serializer used to manage tickets
class TicketSerializer(serializers.ModelSerializer):

    #Fields used to manage forein keys
    user_id = serializers.IntegerField(source = 'account_id.id')
    movie_title = serializers.CharField(source = 'movie_id.title')

    class Meta:
        model = Ticket
        fields = ['id', 'user_id', 'movie_title']


        