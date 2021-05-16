from rest_framework import serializers

from .models import *

class BasicMovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ['id','title', 'price']

class DetailMovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ['id','title', 'price', 'rating', 'description']

class TicketSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(source = 'account_id.id')
    movie_title = serializers.CharField(source = 'movie_id.title')

    class Meta:
        model = Ticket
        fields = ['id', 'user_id', 'movie_title']


        