# Generated by Django 2.2.7 on 2023-02-07 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0006_project_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='projectName',
            field=models.CharField(max_length=200),
        ),
    ]