# Generated by Django 2.2.4 on 2019-08-20 03:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0006_auto_20190820_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='genre',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 8, 20, 3, 37, 47, 489404, tzinfo=utc)),
        ),
    ]
