# Generated by Django 2.0.7 on 2019-01-17 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TheaterWinBook', '0020_auto_20190117_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theaterwinquestioninfo',
            name='question_fk',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='TheaterWinBook.TheaterWinQuestion'),
        ),
    ]