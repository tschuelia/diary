# Generated by Django 3.1.2 on 2020-10-04 13:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diary", "0002_auto_20201004_1256"),
    ]

    operations = [
        migrations.AddField(
            model_name="diary",
            name="location_alias",
            field=models.CharField(
                default="Kein Orts-Alias angegeben",
                max_length=255,
                verbose_name="Ortsbezeichnung",
            ),
        ),
    ]
