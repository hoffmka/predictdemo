# Generated by Django 2.2.7 on 2023-01-20 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0004_auto_20201216_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='description',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='model',
            name='doi',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
