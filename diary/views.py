from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import DeleteView

from .models import Diary, Entry, get_diaries_for_user
from .forms import DiaryForm, EntryForm, ImageFormSet, FileFormSet

from django.conf import settings


@login_required
def diaries_overview(request):
    diaries = get_diaries_for_user(request.user)

    diaries_and_images = [(d, d.get_images().order_by("?").first()) for d in diaries]
    return render(
        request,
        "diary/diaries_overview.html",
        {
            "diaries_and_images": diaries_and_images,
        },
    )


@login_required
def diary_detail(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    entries = diary.get_entries()
    entries_and_images = [(e, e.get_images().order_by("?").first()) for e in entries]
    locations = [(e.location.x, e.location.y) for e in entries]
    labels = [e.title for e in entries]
    urls = [
        reverse("entry-detail", kwargs={"diary_pk": pk, "entry_pk": e.pk})
        for e in entries
    ]

    return render(
        request,
        "diary/diary_detail.html",
        {
            "diary": diary,
            "diary_location": (diary.location.x, diary.location.y),
            "entries_and_images": entries_and_images,
            "locations": locations,
            "labels": labels,
            "urls": urls,
            "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
        },
    )


@login_required
def diary_gallery(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    entries = diary.get_entries()
    entries_and_images = [(e, e.get_images()) for e in entries]
    return render(
        request,
        "diary/diary_gallery.html",
        {"diary": diary, "entries_and_images": entries_and_images},
    )


@login_required
def diary_create(request):
    if request.method == "GET":
        form = DiaryForm()
        return render(request, "diary/diary_form.html", {"form": form})
    else:
        form = DiaryForm(request.POST)
        form.instance.owner = request.user
        diary = form.save()
        return redirect("diary-detail", pk=diary.pk)


@login_required
def diary_update(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    if diary.owner != request.user:
        raise PermissionDenied

    if request.method == "GET":
        form = DiaryForm(instance=diary)
        return render(request, "diary/diary_form.html", {"form": form})
    else:
        form = DiaryForm(request.POST, instance=diary)
        form.instance.owner = request.user
        diary = form.save()
        return redirect("diary-detail", pk=diary.pk)


class DiaryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Diary
    success_url = "/"

    def test_func(self):
        diary = self.get_object()
        return self.request.user == diary.owner


@login_required
def entry_detail(request, diary_pk, entry_pk):
    diary = get_object_or_404(Diary, pk=diary_pk)
    entry = get_object_or_404(Entry, pk=entry_pk)
    entry_location = (entry.location.x, entry.location.y)
    images = entry.get_images()
    files = entry.get_files()

    return render(
        request,
        "diary/entry_detail.html",
        {
            "diary": diary,
            "entry": entry,
            "entry_location": entry_location,
            "images": images,
            "files": files,
            "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
        },
    )


@login_required
def create_entry(request, pk):
    diary = get_object_or_404(Diary, pk=pk)

    if diary.owner != request.user:
        raise PermissionDenied

    if request.method == "GET":
        entry_form = EntryForm()
        image_formset = ImageFormSet()
        file_formset = FileFormSet()
        return render(
            request,
            "diary/entry_form.html",
            {"entry_form": entry_form, "images": image_formset},
        )
    else:
        entry_form = EntryForm(request.POST)
        image_formset = ImageFormSet(request.POST)
        file_formset = FileFormSet(request.POST)
        entry_form.instance.diary = diary
        if not entry_form.is_valid():
            return render(
                request,
                "diary/entry_form.html",
                {"entry_form": entry_form, "images": image_formset},
            )
        entry_form.save()
        return redirect("diary-detail", pk=pk)


@login_required
def update_entry(request, diary_pk, entry_pk):
    diary = get_object_or_404(Diary, pk=diary_pk)
    entry = get_object_or_404(Entry, pk=entry_pk)

    if diary.owner != request.user:
        raise PermissionDenied

    if request.method == "GET":
        entry_form = EntryForm(instance=entry)
        return render(request, "diary/entry_form.html", {"entry_form": entry_form})
    else:
        entry_form = EntryForm(request.POST, instance=entry)
        entry_form.instance.diary = diary
        entry = entry_form.save()
        return redirect("entry-detail", diary_pk=diary_pk, entry_pk=entry_pk)


@login_required
def delete_entry(request, diary_pk, entry_pk):
    diary = get_object_or_404(Diary, pk=diary_pk)
    if diary.owner != request.user:
        raise PermissionDenied

    entry = get_object_or_404(Entry, pk=entry_pk)

    if request.method == "GET":
        return render(request, "diary/entry_confirm_delete.html", {"entry": entry})
    else:
        entry.delete()
        return redirect("diary-detail", pk=diary_pk)


@login_required
def add_images_to_entry(request, diary_pk, entry_pk):
    diary = get_object_or_404(Diary, pk=diary_pk)
    if diary.owner != request.user:
        raise PermissionDenied

    entry = get_object_or_404(Entry, pk=entry_pk)

    if request.method == "GET":
        formset = ImageFormSet(instance=entry)
        return render(request, "diary/entry_images_form.html", {"formset": formset})
    else:
        formset = ImageFormSet(request.POST, request.FILES, instance=entry)
        if not formset.is_valid():
            return render(request, "diary/entry_images_form.html", {"formset": formset})
        formset.save()
        return redirect("entry-detail", diary_pk=diary_pk, entry_pk=entry_pk)


@login_required
def add_files_to_entry(request, diary_pk, entry_pk):
    diary = get_object_or_404(Diary, pk=diary_pk)
    if diary.owner != request.user:
        raise PermissionDenied

    entry = get_object_or_404(Entry, pk=entry_pk)

    if request.method == "GET":
        formset = FileFormSet(instance=entry)
        return render(request, "diary/entry_files_form.html", {"formset": formset})
    else:
        formset = FileFormSet(request.POST, request.FILES, instance=entry)
        if not formset.is_valid():
            return render(request, "diary/entry_files_form.html", {"formset": formset})
        formset.save()
        return redirect("entry-detail", diary_pk=diary_pk, entry_pk=entry_pk)


@login_required
def map_view(request):
    diaries = Diary.objects.all()
    showOnlyOwnDiaries = "onlyOwnDiaries" in request.GET

    if showOnlyOwnDiaries:
        diaries = diaries.filter(owner=request.user)

    locations = [(d.location.x, d.location.y) for d in diaries]
    labels = [d.title for d in diaries]
    urls = [reverse("diary-detail", kwargs={"pk": d.pk}) for d in diaries]
    return render(
        request,
        "diary/map_view.html",
        {
            "locations": locations,
            "labels": labels,
            "urls": urls,
            "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
            "onlyOwnDiariesSelected": showOnlyOwnDiaries,
        },
    )
