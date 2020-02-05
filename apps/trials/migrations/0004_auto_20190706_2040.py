# Generated by Django 2.2.1 on 2019-07-06 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trials', '0003_trial_createdby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trial',
            name='clinicalTrials',
            field=models.CharField(default=None, max_length=40),
        ),
        migrations.AlterField(
            model_name='trial',
            name='description',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='trial',
            name='eudraCT',
            field=models.CharField(default=None, max_length=40),
        ),
    ]