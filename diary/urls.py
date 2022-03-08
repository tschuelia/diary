from django.urls import path

from . import views
from .views import DiaryDeleteView

urlpatterns = [
    path("", views.diaries_overview, name="diaries-overview"),
    path("map", views.map_view, name="map-view"),
    path("diary/<int:pk>", views.diary_detail, name="diary-detail"),
    path("diary/create", views.diary_create, name="diary-create"),
    path("diary/<int:pk>/update", views.diary_update, name="diary-update"),
    path("diary/<int:pk>/delete", DiaryDeleteView.as_view(), name="diary-delete"),
    path("diary/<int:pk>/addEntry", views.create_entry, name="create-entry"),
    path("diary/<int:pk>/gallery", views.diary_gallery, name="diary-gallery"),
    path(
        "diary/<int:diary_pk>/entry/<int:entry_pk>",
        views.entry_detail,
        name="entry-detail",
    ),
    path(
        "diary/<int:diary_pk>/entry/<int:entry_pk>/update",
        views.update_entry,
        name="update-entry",
    ),
    path(
        "diary/<int:diary_pk>/entry/<int:entry_pk>/delete",
        views.delete_entry,
        name="delete-entry",
    ),
    path(
        "diary/<int:diary_pk>/entry/<int:entry_pk>/addimages",
        views.add_images_to_entry,
        name="add-images",
    ),
    path(
        "diary/<int:diary_pk>/entry/<int:entry_pk>/addfiles",
        views.add_files_to_entry,
        name="add-files",
    ),
]
