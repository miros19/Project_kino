from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import api_view

import jwt

from .models import *
from .serializers import *


@api_view(['GET',])
def show_all_movies(request):
    movies = Movie.objects.all()

    serializer = BasicMovieSerializer(movies, many = True)

    return Response(serializer.data)


@api_view(['GET',])
def show_my_movies(request):
    if request.method == "GET":

        cookie = request.COOKIES.get('jwt')

        if not cookie:
            raise AuthenticationFailed("User not authenticated!")
        
        else:
            try:
                payLoad = jwt.decode(cookie, 'key256', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("User not authenticated!")

            user_id = Account.objects.get(id = payLoad['id'])

            tickets = Ticket.objects.filter(account_id_id = user_id)

            serializer = TicketSerializer(tickets, many = True)

            return Response(serializer.data)

@api_view(["POST",])
def show_movie_details(request):
    if request.method == "POST":
        id = request.data['id']

        movie = Movie.objects.get(id = id)

        if movie is None:
            raise NotFound("There is no such movie!")
        else:
            serializer = DetailMovieSerializer(movie)
            return Response(serializer.data)

@api_view(["POST",])
def buy_movie(request):
    if request.method == "POST":

        cookie = request.COOKIES.get('jwt')

        if not cookie:
            raise AuthenticationFailed("User not authenticated!")
        
        else:
            try:
                payLoad = jwt.decode(cookie, 'key256', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("User not authenticated!")

            movie_id = request.data['id']

            user = Account.objects.get(id = payLoad['id'])
            movie = Movie.objects.get(id = movie_id)

            if movie is None:
                raise NotFound("There is no such movie!")
            else:
                if user.funds < movie.price:
                    raise PermissionDenied("Insufficient funds!")
                else:
                    ticket = Ticket()
                    ticket.account_id = user
                    ticket.movie_id = movie
                    user.funds -= movie.price
                    user.save()
                    ticket.save()
                    
                    return Response({
                            "Message": "Ticket bought!"
                        })

