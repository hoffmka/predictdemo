# Generated by Django 2.2.7 on 2020-04-28 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TreatMedication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('targetId', models.CharField(max_length=40)),
                ('dateBegin', models.DateField()),
                ('dateEnd', models.DateField(blank=True)),
                ('interval', models.IntegerField()),
                ('intervalUnit', models.IntegerField()),
                ('drugName', models.CharField(max_length=40)),
                ('dosage', models.IntegerField()),
                ('dosageUnit', models.CharField(max_length=20)),
                ('medScheme', models.CharField(max_length=100)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
