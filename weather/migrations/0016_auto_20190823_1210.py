# Generated by Django 2.2.4 on 2019-08-23 12:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0015_auto_20190823_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='weatherId',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 23, 12, 10, 10, 903916, tzinfo=utc)),
        ),
    ]
