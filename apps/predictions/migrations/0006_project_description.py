# Generated by Django 2.2.7 on 2023-01-20 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0005_auto_20230120_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
    ]
