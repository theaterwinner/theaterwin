# Generated by Django 2.1.2 on 2018-12-24 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TheaterWinBook', '0012_post_created_date2'),
    ]

    operations = [
        migrations.AddField(
            model_name='theaterwinquestion',
            name='question_thumbup2',
            field=models.IntegerField(default=0),
        ),
    ]