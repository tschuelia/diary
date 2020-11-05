# Generated by Django 3.1.2 on 2020-10-08 17:02

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0007_auto_20201008_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='description',
            field=models.TextField(blank=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AddField(
            model_name='image',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]