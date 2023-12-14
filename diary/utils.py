import cv2
import datetime
import ffmpeg
import PIL
import PIL.ExifTags

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


def _image_exif_data(pil_image):
    if pil_image._getexif():
        return {PIL.ExifTags.TAGS[k]: v for k, v in pil_image._getexif().items() if k in PIL.ExifTags.TAGS}


def get_image_date_and_dimensions(image):
    """
    Returns the datetime when the image was taken if the image has exif data.
    """
    pil_image = PIL.Image.open(image)
    exif = _image_exif_data(pil_image)

    creation_time = None

    # check if image has exif data
    if exif and "DateTimeOriginal" in exif.keys():
        dtorig = exif["DateTimeOriginal"]
        # DateTimeOriginal is of format "2019:01:11 11:08:47"
        creation_time = datetime.datetime.strptime(dtorig, "%Y:%m:%d %H:%M:%S")

    if exif and "Orientation" in exif.keys() and (exif["Orientation"] == 6 or exif["Orientation"] == 8):
        # (height, width)
        height, width = pil_image.size[0], pil_image.size[1]

    else:
        height, width = pil_image.size[1], pil_image.size[0]

    return creation_time, height, width


def get_video_date_and_dimensions(video_path):
    data = ffmpeg.probe(video_path).get("streams", [])
    width = None
    height = None
    creation_time = None
    for d in data:
        width = d.get("width", width)
        height = d.get("height", height)
        creation_time = d.get("tags", {}).get("creation_time")

    if creation_time:
        creation_time = datetime.datetime.fromisoformat(creation_time)

    return creation_time, height, width


def get_video_thumbnail(video_path):
    # read the first frame of the video and return it as django ImageField
    vidcap = cv2.VideoCapture(video_path)
    _, frame = vidcap.read()
    vidcap.release()
    pil_image = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # tmp_file = cv2.imwrite("tmp_file.jpg", frame)
    tmp_file = BytesIO()
    pil_image.save(tmp_file, format="JPEG")
    tmp_file = ContentFile(tmp_file.getvalue())
    return InMemoryUploadedFile(tmp_file, None, "tmp_file.jpg", "image/jpeg", tmp_file.tell, None)
