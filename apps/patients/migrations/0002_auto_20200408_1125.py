# Generated by Django 2.2.7 on 2020-04-08 11:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PredictionModel',
            new_name='Prediction',
        ),
    ]
