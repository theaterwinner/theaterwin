# Generated by Django 2.0.7 on 2019-01-27 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TheaterWinBook', '0022_theaterwinquestionreply'),
    ]

    operations = [
        migrations.AddField(
            model_name='theaterwinquestionreply',
            name='reply_groupnum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='theaterwinquestionreply',
            name='reply_level_ingorup',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='theaterwinquestionreply',
            name='reply_sequencenum_ingroup',
            field=models.IntegerField(default=0),
        ),
    ]