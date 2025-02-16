FROM python:3

RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin ffmpeg libsm6 libxext6
RUN apt-get install libsqlite3-mod-spatialite
RUN mkdir /app

RUN python -m venv /app/venv \
 && /app/venv/bin/pip install -U pip
COPY requirements.txt requirements-deploy.txt /tmp/
RUN /app/venv/bin/pip install -r /tmp/requirements.txt \
 && /app/venv/bin/pip install -r /tmp/requirements-deploy.txt

COPY diary /app/diary/diary
COPY diaryWebsite /app/diary/diaryWebsite
COPY run.sh diaryWebsite/settings.py /app/diary/

CMD ["bash", "-xeu", "/app/diary/run.sh"]
