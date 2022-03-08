from django import forms
from django.forms import inlineformset_factory

from bootstrap_datepicker_plus import DateTimePickerInput
from pagedown.widgets import AdminPagedownWidget, PagedownWidget
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Diary, Entry, Image, File
from .utils import get_image_date, get_image_size


class DiaryForm(forms.ModelForm):
    summary = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Diary
        exclude = ("owner",)
        widgets = {
            "location": GooglePointFieldWidget,
            "start_date": DateTimePickerInput(format="%Y-%m-%d"),
            "end_date": DateTimePickerInput(format="%Y-%m-%d"),
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
            "start_date": DateTimePickerInput(format="%Y-%m-%d"),
            "end_date": DateTimePickerInput(format="%Y-%m-%d"),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image", "description"]

    def save(self, *args, **kwargs):
        kwargs["commit"] = False
        image_obj = super().save(*args, **kwargs)
        if "image" in self.changed_data:
            image_obj.date = get_image_date(image_obj.image)
            image_size = get_image_size(image_obj.image)
            image_obj.height = image_size[0]
            image_obj.width = image_size[1]

        image_obj.save()
        return image_obj


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file", "filename", "description"]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


ImageFormSet = inlineformset_factory(
    Entry,
    Image,
    form=ImageForm,
    fields=("image", "description"),
    can_delete=True,
    extra=1,
)

FileFormSet = inlineformset_factory(
    Entry,
    File,
    form=FileForm,
    fields=("file", "filename", "description"),
    can_delete=True,
    extra=1,
)