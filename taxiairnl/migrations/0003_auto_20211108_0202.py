# Generated by Django 3.1.4 on 2021-11-07 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiairnl', '0002_auto_20211108_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip_details',
            name='is_babystoel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trip_details',
            name='is_return',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trip_details',
            name='remarks',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
