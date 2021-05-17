from rest_framework import serializers

from .models import *

#Serializer created to register a user
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'}, write_only = True)

    class Meta:
        model = Account
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    #Overriting save() method to save user to database
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

#Serializer created to display user's account
class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ['id', 'email', 'name', 'funds']

#Serializer created to update user's funds  
class FundsSerializer(serializers.Serializer):

    funds = serializers.IntegerField()