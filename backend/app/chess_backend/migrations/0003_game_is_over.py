# Generated by Django 4.0 on 2021-12-22 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess_backend', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_over',
            field=models.BooleanField(default=False),
        ),
    ]
