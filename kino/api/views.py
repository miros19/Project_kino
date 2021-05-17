from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

import jwt
import datetime

from .models import Account
from .serializers import *

#View used to register user
@api_view(['POST',])
def registration_view(request):
    #Double checking method (I know it's unnecessary)
    if request.method == 'POST':
        #Getting JSON data
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        #If data is valid, create new user and return response, else return error
        if serializer.is_valid():  

            account = serializer.save()
            data['response'] = "Successfully created a new user"
            data['email'] = account.email
            data['name'] = account.name

        else:

            data = serializer.errors

        return Response(data)

#View used to login user using the JWT token
@api_view(['POST',])
def login_view(request):
    #Double checking method (I know it's unnecessary)
    if request.method == "POST":
        email = request.data['email']
        password = request.data['password']

        user = Account.objects.get(email = email)
        #Checking if user exists
        if user is None:
            raise AuthenticationFailed("User does not exist!")
        #Checking if password is valid
        elif not user.check_password(password):
            raise AuthenticationFailed("Password incorrect!")

        else:
            #Creating payload for JWT token
            payLoad = {
                'id' : user.id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat' : datetime.datetime.utcnow()
            }
            #Creating token
            token = jwt.encode(payLoad,'key256', algorithm='HS256')
            #Sending token to user via cookie
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                "jwt": token
            }

            return response

#View used to see user's profile
@api_view(['GET',])
def account_view(request):
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
            #Getting user's data 
            user = Account.objects.get(id = payLoad['id'])

            serializer = AccountSerializer(user)

            return Response(serializer.data)

#Logging out user via deleting JWT token
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'Message': 'Logged out!'
        }
        return response

#View used to add more funds to user's wallet
class AddFunds(APIView):
    def post(self, request):
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
            #Adding new funds to user's wallet
            serializer = FundsSerializer(data = request.data)
            response = Response()
            if serializer.is_valid():
                user = Account.objects.get(id = payLoad['id'])
                funds = serializer['funds'].value
                user.funds += funds
                user.save()
                response.data = {
                    'Message': 'Funds added successfully!'
                }
            else:
                response.data = {
                    'Message': 'Error adding funds!'
                }
            return response


