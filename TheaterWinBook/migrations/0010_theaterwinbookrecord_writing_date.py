# Generated by Django 2.0.7 on 2018-08-04 03:25

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('TheaterWinBook', '0009_auto_20180802_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='theaterwinbookrecord',
            name='writing_date',
            field=models.DateField(default=django.utils.datetime_safe.datetime.now),
        ),
    ]