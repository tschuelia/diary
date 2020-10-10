from django import forms
from django.forms import inlineformset_factory

from pagedown.widgets import AdminPagedownWidget, PagedownWidget
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Diary, Entry, Image


import PIL
import PIL.ExifTags
from datetime import datetime


class DiaryForm(forms.ModelForm):
    summary = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Diary
        fields = "__all__"
        widgets = {
            "location": GooglePointFieldWidget,
        }


class EntryForm(forms.ModelForm):
    summary = forms.CharField(widget=PagedownWidget())
    description = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Entry
        fields = [
            "title",
            "start_date",
            "end_date",
            "location",
            "summary",
            "description",
        ]
        widgets = {
            "location": GooglePointFieldWidget,
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image", "description"]

    def save(self, *args, **kwargs):
        image_obj = super().save(commit=False)
        if "image" in self.changed_data:
            image = PIL.Image.open(image_obj.image)
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in image._getexif().items()
                if k in PIL.ExifTags.TAGS
            }
            if "DateTimeOriginal" in exif.keys():
                dtorig = exif["DateTimeOriginal"]
                # DateTimeOriginal is of format "2019:01:11 11:08:47"
                image_obj.date = datetime.strptime(dtorig, "%Y:%m:%d %H:%M:%S")
            # TODO: process geolocation information

        image_obj.save()
        return image_obj


ImageFormSet = inlineformset_factory(
    Entry,
    Image,
    form=ImageForm,
    fields=("image", "description"),
    can_delete=True,
    extra=1,
)