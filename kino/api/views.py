from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import jwt
import datetime

from rest_framework.views import APIView

from .models import Account
from .serializers import *

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        
        if serializer.is_valid():
            
            account = serializer.save()
            data['response'] = "Successfully created a new user"
            data['email'] = account.email
            data['name'] = account.name
        else:
            data = serializer.errors
        return Response(data)

@api_view(['POST',])
def login_view(request):
    if request.method == "POST":
        email = request.data['email']
        password = request.data['password']

        user = Account.objects.get(email = email)

        if user is None:
            raise AuthenticationFailed("User does not exist!")
        
        elif not user.check_password(password):
            raise AuthenticationFailed("Password incorrect!")

        else:

            payLoad = {
                'id' : user.id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat' : datetime.datetime.utcnow()
            }

            token = jwt.encode(payLoad,'key256', algorithm='HS256')

            response = Response()

            response.set_cookie(key='jwt', value=token, httponly=True)
            
            response.data = {
                "jwt": token
            }

            return response

@api_view(['GET',])
def account_view(request):
    if request.method == "GET":

        cookie = request.COOKIES.get('jwt')

        if not cookie:
            raise AuthenticationFailed("User not authenticaded!")
        
        else:
            try:
                payLoad = jwt.decode(cookie, 'key256', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("User not authenticaded!")
            user = Account.objects.get(id = payLoad['id'])
            
            data = {'id': user.id, 'name': user.name, 'email':user.email, 'tickets': []}

            serializer = AccountSerializer(data)

            print(serializer.data)

            return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'Message': 'Logged out!'
        }
        return response
