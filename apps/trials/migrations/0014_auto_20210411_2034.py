# Generated by Django 2.2.7 on 2021-04-11 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trials', '0013_trial_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trial',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]