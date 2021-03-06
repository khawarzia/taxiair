# Generated by Django 3.1.4 on 2021-11-07 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='registered_riders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=500, null=True)),
                ('email', models.CharField(blank=True, max_length=500, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=500, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=400, null=True)),
                ('email', models.CharField(blank=True, max_length=400, null=True)),
                ('name', models.CharField(blank=True, max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='trip_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_loc', models.CharField(blank=True, max_length=500, null=True)),
                ('to_loc', models.CharField(blank=True, max_length=500, null=True)),
                ('date_time', models.DateTimeField(blank=True, null=True)),
                ('vehicle', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.CharField(blank=True, max_length=100, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_local', models.BooleanField(default=False)),
                ('dist', models.CharField(blank=True, max_length=100, null=True)),
                ('timet', models.CharField(blank=True, max_length=100, null=True)),
                ('objnum', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='taxiairnl.user_details')),
            ],
        ),
    ]
