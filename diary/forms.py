import pathlib

from django import forms
from django.forms import inlineformset_factory

from pagedown.widgets import PagedownWidget
from mapwidgets.widgets import GoogleMapPointFieldWidget

from .models import Diary, Entry, Image, File
from .utils import get_image_date_and_dimensions, get_video_date_and_dimensions, get_video_thumbnail

from diaryWebsite.settings_base import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS


class DateInput(forms.DateInput):
    input_type = "date"


class DiaryForm(forms.ModelForm):
    summary = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Diary
        exclude = ("owner",)
        widgets = {
            "location": GoogleMapPointFieldWidget,
            "start_date": DateInput(format=("%Y-%m-%d")),
            "end_date": DateInput(format=("%Y-%m-%d"))
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
            "location": GoogleMapPointFieldWidget,
            "start_date": DateInput(format=("%Y-%m-%d")),
            "end_date": DateInput(format=("%Y-%m-%d")),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image", "description"]

    def save(self, *args, **kwargs):
        kwargs["commit"] = False
        image_obj = super().save(*args, **kwargs)
        if "image" in self.changed_data:
            # check if the uploaded file is an image or a video
            file_extension = pathlib.Path(image_obj.image.url).suffix[1:].lower()
            if file_extension in IMAGE_EXTENSIONS:
                image_obj.date, image_obj.height, image_obj.width = get_image_date_and_dimensions(image_obj.image)
                image_obj.is_image = True
            elif file_extension in VIDEO_EXTENSIONS:
                temporary_video_path = self.cleaned_data["image"].temporary_file_path()
                image_obj.date, image_obj.height, image_obj.width = get_video_date_and_dimensions(temporary_video_path)
                image_obj.is_image = False

                # thumbnail to display in the gallery
                thumbnail = get_video_thumbnail(temporary_video_path)
                image_obj.video_thumbnail.save(
                    f"{pathlib.Path(image_obj.image.url).stem}_thumbnail.jpg",
                    thumbnail
                )
            else:
                raise ValueError("Unsupported file format: ", file_extension)
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