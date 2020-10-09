from django.contrib import admin
from django.contrib.gis.db import models


from .models import Diary, Entry, Image
from .forms import DiaryForm, EntryForm

from mapwidgets.widgets import GooglePointFieldWidget


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    formfield_overrides = {models.PointField: {"widget": GooglePointFieldWidget}}
    form = DiaryForm
    fields = [
        "title",
        "owner",
        "start_date",
        "end_date",
        "location_alias",
        "location",
        "summary",
    ]


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    formfield_overrides = {models.PointField: {"widget": GooglePointFieldWidget}}
    form = EntryForm
    fields = [
        "diary",
        "title",
        "start_date",
        "end_date",
        "location",
        "description",
        "participants",
    ]

admin.site.register(Image)