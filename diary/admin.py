from django.contrib import admin
from django.contrib.gis.db import models


from .models import Diary, Entry, Image
from .forms import DiaryForm, EntryForm

from mapwidgets.widgets import GoogleMapPointFieldWidget


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    formfield_overrides = {models.PointField: {"widget": GoogleMapPointFieldWidget}}
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
    formfield_overrides = {models.PointField: {"widget": GoogleMapPointFieldWidget}}
    form = EntryForm
    fields = [
        "diary",
        "title",
        "start_date",
        "end_date",
        "location",
        "summary",
        "description",
    ]


admin.site.register(Image)
