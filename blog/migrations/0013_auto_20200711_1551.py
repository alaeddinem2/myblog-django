# Generated by Django 3.0.7 on 2020-07-11 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_weather'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Weather',
            new_name='City',
        ),
    ]