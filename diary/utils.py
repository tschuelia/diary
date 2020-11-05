import PIL
import PIL.ExifTags
from datetime import datetime


def _image_exif_data(pil_image):
    if pil_image._getexif():
        return {
            PIL.ExifTags.TAGS[k]: v
            for k, v in pil_image._getexif().items()
            if k in PIL.ExifTags.TAGS
        }


def get_image_date(image):
    """
    Returns the datetime when the image was taken if the image has exif data.
    """
    pil_image = PIL.Image.open(image)
    exif = _image_exif_data(pil_image)
    # check if image has exif data
    if exif and "DateTimeOriginal" in exif.keys():
        dtorig = exif["DateTimeOriginal"]
        # DateTimeOriginal is of format "2019:01:11 11:08:47"
        return datetime.strptime(dtorig, "%Y:%m:%d %H:%M:%S")


def get_image_size(image):
    """
    Returns the size of the image. The image size depends whether the image is rotated.
    This is indicated by the exif "Orientation" key.
    6 means the image is rotated by 90 degrees
    8 means the image is rotated by 270 degrees
    In both cases height and width of the image need to be flipped.
    """
    pil_image = PIL.Image.open(image)
    exif = _image_exif_data(pil_image)
    # check if image has exif data
    if (
        exif
        and "Orientation" in exif.keys()
        and (exif["Orientation"] == 6 or exif["Orientation"] == 8)
    ):
        # (height, width)
        return (pil_image.size[0], pil_image.size[1])

    return (pil_image.size[1], pil_image.size[0])
