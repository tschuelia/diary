# Generated by Django 3.1.2 on 2020-10-04 12:56

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("diary", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="diary",
            name="summary",
            field=models.TextField(blank=True, verbose_name="Zusammenfassung"),
        ),
        migrations.AlterField(
            model_name="diary",
            name="end_date",
            field=models.DateField(blank=True, verbose_name="Enddatum"),
        ),
        migrations.AlterField(
            model_name="diary",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Titel"),
        ),
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Titel")),
                ("start_date", models.DateField(verbose_name="Startdatum")),
                ("end_date", models.DateField(blank=True, verbose_name="Enddatum")),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        srid=4326, verbose_name="Ort"
                    ),
                ),
                (
                    "participants",
                    models.CharField(max_length=255, verbose_name="Teilnehmer"),
                ),
                ("description", models.TextField(verbose_name="Beschreibung")),
                (
                    "diary",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entry_of",
                        to="diary.diary",
                        verbose_name="Tagebucheintrag",
                    ),
                ),
            ],
        ),
    ]
