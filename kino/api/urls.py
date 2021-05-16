from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('register', registration_view, name = 'register'),
    path('login', login_view, name = 'login'),
    path('logout', LogoutView.as_view(), name = 'logout'),
    path('account', account_view, name = 'account'),
]