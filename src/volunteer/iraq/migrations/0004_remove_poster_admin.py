# Generated by Django 3.1.2 on 2021-09-23 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iraq', '0003_poster_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poster',
            name='admin',
        ),
    ]
