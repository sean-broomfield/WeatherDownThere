# Generated by Django 2.2.4 on 2019-08-23 10:43

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0012_auto_20190822_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 23, 10, 42, 59, 891298, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('description', models.CharField(default='', max_length=255)),
                ('temphi', models.IntegerField(default='')),
                ('templow', models.IntegerField(default='')),
                ('icon', models.URLField(default='')),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.Event')),
            ],
        ),
    ]
