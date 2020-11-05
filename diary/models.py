from django.db import models
from django.contrib.gis.db import models as gisModels
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User

from datetime import datetime


class Diary(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titel")
    start_date = models.DateField(verbose_name="Startdatum")
    end_date = models.DateField(blank=True, verbose_name="Enddatum")
    location = gisModels.PointField(verbose_name="Ort")
    location_alias = models.CharField(
        max_length=255,
        default="Kein Orts-Alias angegeben",
        verbose_name="Ortsbezeichnung",
    )
    summary = models.TextField(blank=True, verbose_name="Zusammenfassung")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)

    def __str__(self):
        return self.title

    def get_entries(self):
        return self.entry_of.all().order_by("start_date")

    def get_images(self):
        entry_pks = [e.pk for e in self.get_entries()]
        return Image.objects.filter(entry__in=entry_pks)


class Entry(models.Model):
    diary = models.ForeignKey(
        Diary,
        on_delete=models.CASCADE,
        verbose_name="Tagebucheintrag",
        related_name="entry_of",
    )
    title = models.CharField(max_length=255, verbose_name="Titel")
    start_date = models.DateField(verbose_name="Startdatum")
    end_date = models.DateField(blank=True, null=True, verbose_name="Enddatum")
    location = gisModels.PointField(verbose_name="Ort")
    summary = models.TextField(blank=True, verbose_name="Zusammenfassung")
    description = models.TextField(verbose_name="Beschreibung")

    def __str__(self):
        return self.title

    def get_images(self):
        return self.image_of.all().order_by("date")


class Image(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    image = models.ImageField(
        default="default.jpg",
        upload_to="entry_pics",
        verbose_name="Bilder",
    )
    entry = models.ForeignKey(
        Entry, related_name="image_of", on_delete=models.CASCADE, null=True
    )
    description = models.TextField(blank=True, verbose_name="Bildbeschreibung")
    date = models.DateTimeField(blank=True, null=True)
    location = gisModels.PointField(blank=True, null=True)

    def __str__(self):
        return self.entry.title

    def get_url(self):
        return self.image.url

    def get_date(self):
        if not self.date:
            return self.entry.start_date
        return self.date

    def get_location(self):
        if not self.location:
            return self.entry.location
        return self.location
