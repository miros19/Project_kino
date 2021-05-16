from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.deletion import CASCADE
from api.models import Account

# Create your models here.

class Movie(models.Model):
    id = models.IntegerField(primary_key=True, unique = True)
    title = models.CharField(verbose_name="Title", max_length=30,unique=True)
    price = models.IntegerField()
    rating = models.PositiveBigIntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    description = models.TextField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title

class Ticket(models.Model):
    id = models.IntegerField(primary_key=True, unique = True)
    account_id = models.ForeignKey(Account, on_delete=CASCADE, verbose_name="User")
    movie_id = models.ForeignKey(Movie, on_delete=CASCADE, verbose_name="Movie")