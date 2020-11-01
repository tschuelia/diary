from .settings_base import *

SECRET_KEY = "4l1z+^kbiy^mz9=@ysd8h!y#-%hb!-zo&3wisp$#z5fd6yw%0u"
ALLOWED_HOSTS = []
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

GOOGLE_MAP_API_KEY = "YOUR API KEY"
MAP_WIDGETS["GOOGLE_MAP_API_KEY"] = GOOGLE_MAP_API_KEY
