# Generated by Django 3.2.3 on 2021-05-15 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
