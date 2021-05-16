# Generated by Django 3.2.3 on 2021-05-16 08:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='Title')),
                ('price', models.IntegerField()),
                ('rating', models.PositiveBigIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('description', models.TextField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Movie',
                'verbose_name_plural': 'Movies',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('account_id', models.IntegerField()),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
    ]