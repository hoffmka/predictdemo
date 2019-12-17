# Generated by Django 2.2.1 on 2019-07-06 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trials', '0002_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='trial',
            name='createdBy',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
