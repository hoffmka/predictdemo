# Generated by Django 2.2.7 on 2020-05-08 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0002_auto_20200505_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='status',
            field=models.IntegerField(choices=[(0, 'started'), (1, 'finished'), (2, 'failed')], default=0),
        ),
    ]