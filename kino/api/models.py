from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#Custom menager created to manage custom user model
class MyAccountManager(BaseUserManager):
    #Overriting create_superuser method with custom model
    def create_superuser(self, email, password, name):
        user = self.create_user(
            name = name,
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

#Custom user model containing desired fields
class Account(AbstractBaseUser):
    id = models.IntegerField(primary_key=True, unique=True )
    email = models.EmailField(verbose_name="E-mail", unique=True)
    name = models.CharField(verbose_name="Name", max_length=20)
    funds = models.IntegerField(default = 0)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    objects = MyAccountManager()

    #STR method for clean view
    def __str__(self):
        return self.name

    # Names used to display in admin panel
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


    

