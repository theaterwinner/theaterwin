# Generated by Django 2.0.7 on 2018-07-30 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TheaterWinBook', '0003_testmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TheaterBook',
            new_name='TheaterWinBookRecord',
        ),
    ]