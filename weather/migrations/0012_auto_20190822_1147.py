# Generated by Django 2.2.4 on 2019-08-22 11:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0011_auto_20190822_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='seatMap',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 22, 11, 47, 26, 852536, tzinfo=utc)),
        ),
    ]
