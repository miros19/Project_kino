from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import api_view

import jwt

from .models import *
from .serializers import *

#Getting a list of all available movies
@api_view(['GET',])
def show_all_movies(request):
    movies = Movie.objects.all()

    serializer = BasicMovieSerializer(movies, many = True)

    return Response(serializer.data)

#Getting a list of movies bought by user
@api_view(['GET',])
def show_my_movies(request):
    #Double checking method (I know it's unnecessary)
    if request.method == "GET":
        #Getting user's JWT token
        cookie = request.COOKIES.get('jwt')
        #Checking if token exists
        if not cookie:
            raise AuthenticationFailed("User not authenticated!")
        
        else:
            #Checking if token is valid, if not raising error
            try:
                #Decoding token, to get user's id
                payLoad = jwt.decode(cookie, 'key256', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("User not authenticated!")
            #Getting a given user
            user_id = Account.objects.get(id = payLoad['id'])
            #Getting his tickets
            tickets = Ticket.objects.filter(account_id_id = user_id)
            #Serializing tickets to send
            serializer = TicketSerializer(tickets, many = True)
            #Returning serialized tickets
            return Response(serializer.data)

#Getting movie details
@api_view(["POST",])
def show_movie_details(request):
    #Double checking method (I know it's unnecessary)
    if request.method == "POST":
        #Getting movie id
        id = request.data['id']

        movie = Movie.objects.get(id = id)
        #Checking if movie exists
        if movie is None:
            raise NotFound("There is no such movie!")
        else:
            #Serializing movie data
            serializer = DetailMovieSerializer(movie)
            return Response(serializer.data)

#View used to 
@api_view(["POST",])
def buy_movie(request):
    #Double checking method (I know it's unnecessary)
    if request.method == "POST":
        #Getting user's JWT token
        cookie = request.COOKIES.get('jwt')
        #Checking if token exists
        if not cookie:
            raise AuthenticationFailed("User not authenticated!")
        else:
            #Checking if token is valid, if not raising error
            try:
                payLoad = jwt.decode(cookie, 'key256', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("User not authenticated!")
            #Getting movie id
            movie_id = request.data['id']
            #Getting user and movie
            user = Account.objects.get(id = payLoad['id'])
            movie = Movie.objects.get(id = movie_id)
            #Checking if movie exist
            if movie is None:
                raise NotFound("There is no such movie!")
            else:
                #Checking if user has sufficient funds
                if user.funds < movie.price:
                    raise PermissionDenied("Insufficient funds!")
                else:
                    #Buying a ticket
                    ticket = Ticket()
                    ticket.account_id = user
                    ticket.movie_id = movie
                    user.funds -= movie.price
                    user.save()
                    ticket.save()
                    
                    return Response({
                            "Message": "Ticket bought!"
                        })

