from rest_framework import serializers

from .models import *

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'}, write_only = True)

    class Meta:
        model = Account
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def save(self):
        account = Account(
            email = self.validated_data['email'],
            name = self.validated_data['name'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords don\'t match'})
        
        account.set_password(password)
        account.save()

        return account

class AccountSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    tickets = serializers.ListField(
        child = serializers.CharField(), 
        allow_empty = True
    )
    
