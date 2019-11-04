# Generated by Django 2.2.1 on 2019-07-03 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studyCode', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('clinicalTrials', models.CharField(max_length=40)),
                ('eudraCT', models.CharField(max_length=40)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
