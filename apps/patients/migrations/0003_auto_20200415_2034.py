# Generated by Django 2.2.7 on 2020-04-15 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_auto_20200408_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prediction',
            name='createdBy',
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='model',
        ),
        migrations.DeleteModel(
            name='Model',
        ),
        migrations.DeleteModel(
            name='Prediction',
        ),
    ]
