# Generated by Django 3.2.20 on 2023-12-10 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0011_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='is_image',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='description',
            field=models.TextField(blank=True, verbose_name='Beschreibung'),
        ),
    ]
