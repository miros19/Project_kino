from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password, name):
        if not email:
            raise ValueError("Podaj email")
        if not name:
            raise ValueError("Podaj imię")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
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

class Account(AbstractBaseUser):
    id = models.IntegerField(primary_key=True, unique=True )
    email = models.EmailField(verbose_name="E-mail", unique=True)
    name = models.CharField(verbose_name="Name", max_length=20)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    objects = MyAccountManager()

    def __str__(self):
        return self.name

	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

