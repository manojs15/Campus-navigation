# Generated by Django 5.0 on 2024-07-19 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nav_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('floor', models.IntegerField()),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='nav_app.location')),
            ],
        ),
    ]
