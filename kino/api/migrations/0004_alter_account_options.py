# Generated by Django 3.2.3 on 2021-05-16 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_account_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
