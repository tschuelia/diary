from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

from datetime import datetime

from .models import Diary, Entry


class PermissionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self._dummy_data()

    def _dummy_data(self):
        self.auth_user = User.objects.create_user(
            "auth_user", "auth_user@test.com", "auth_user_pw"
        )
        self.unauth_user = User.objects.create_user(
            "unauth_user", "unauth_user@test.com", "unauth_user_pw"
        )
        self.auth_diary = Diary.objects.create(
            title="Auth_Diary",
            start_date=datetime.now(),
            end_date=datetime.now(),
            location=Point(5, 23),
            location_alias="location_test",
            summary="summary_test",
            owner=self.auth_user,
        )

        self.auth_diary_entry = Entry.objects.create(
            diary=self.auth_diary,
            title="Auth_Diary_Entry",
            start_date=datetime.now(),
            location=Point(0, 0),
            summary="Entry_summary",
            description="Entry Description",
        )

    """
    Tests if diary owner can modify own diaries
    """

    def test_user_can_update_own_diary(self):
        self.client.login(username="auth_user", password="auth_user_pw")
        response = self.client.get(f"/diary/{self.auth_diary.pk}/update")
        self.assertEqual(response.status_code, 200)

    def test_user_can_delete_own_diary(self):
        self.client.login(username="auth_user", password="auth_user_pw")
        response = self.client.get(f"/diary/{self.auth_diary.pk}/delete")
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_entry_for_own_diary(self):
        self.client.login(username="auth_user", password="auth_user_pw")
        response = self.client.get(f"/diary/{self.auth_diary.pk}/addEntry")
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_own_diary_entry(self):
        self.client.login(username="auth_user", password="auth_user_pw")
        response = self.client.get(
            f"/diary/{self.auth_diary.pk}/entry/{self.auth_diary_entry.pk}/update"
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_delete_own_diary_entry(self):
        self.client.login(username="auth_user", password="auth_user_pw")
        response = self.client.get(
            f"/diary/{self.auth_diary.pk}/entry/{self.auth_diary_entry.pk}/delete"
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_add_images_for_own_diary_entry(self):
        self.client.login(username="auth_user", password="auth_user_pw")
        response = self.client.get(
            f"/diary/{self.auth_diary.pk}/entry/{self.auth_diary_entry.pk}/addimages"
        )
        self.assertEqual(response.status_code, 200)

    """
    Tests if user cannot modify other's diaries
    """

    def test_user_cannot_update_others_diary(self):
        self.client.login(username="unauth_user", password="unauth_user_pw")
        response = self.client.get(f"/diary/{self.auth_diary.pk}/update")
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_delete_others_diary(self):
        self.client.login(username="unauth_user", password="unauth_user_pw")
        response = self.client.get(f"/diary/{self.auth_diary.pk}/delete")
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_create_entry_for_others_diary(self):
        self.client.login(username="unauth_user", password="unauth_user_pw")
        response = self.client.get(f"/diary/{self.auth_diary.pk}/addEntry")
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_update_entry_in_others_diary(self):
        self.client.login(username="unauth_user", password="unauth_user_pw")
        response = self.client.get(
            f"/diary/{self.auth_diary.pk}/entry/{self.auth_diary_entry.pk}/update"
        )
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_delete_entry_in_others_diary(self):
        self.client.login(username="unauth_user", password="unauth_user_pw")
        response = self.client.get(
            f"/diary/{self.auth_diary.pk}/entry/{self.auth_diary_entry.pk}/delete"
        )
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_add_images_for_others_diary_entry(self):
        self.client.login(username="unauth_user", password="unauth_user_pw")
        response = self.client.get(
            f"/diary/{self.auth_diary.pk}/entry/{self.auth_diary_entry.pk}/addimages"
        )
        self.assertEqual(response.status_code, 403)
