# Generated by Django 2.0.7 on 2019-01-17 02:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TheaterWinBook', '0019_auto_20190116_2228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theaterwinquestioninfo',
            name='question_hit',
        ),
        migrations.AddField(
            model_name='theaterwinquestion',
            name='question_thumbdown',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='theaterwinquestioninfo',
            name='by_whom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]