
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersCRUDTest(TestCase):
    fixtures = ["test_users.json"]

    def setUp(self):
        self.user = User.objects.create(name="John", email="john@example.com")

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user1 = User.objects.get(pk=1, username="annette")
        cls.user2 = User.objects.get(pk=2, username="superuser")

    def setUp(self):
        self.client.force_login(self.user1)

    def test_create_user_success(self):
        self.client.logout()
        response = self.client.post(reverse("user_create"), {
            "first_name": "Новый",
            "last_name": "Пользователь",
            "username": "newuser123",
            "password1": "SecurePass123",
            "password2": "SecurePass123",
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="newuser123").exists())
        self.assertRedirects(response, reverse("login"))

    def test_update_annette_profile_success(self):
        url = reverse("user_update", kwargs={"pk": self.user1.pk})
        response = self.client.post(url, {
            "first_name": "Обновленный",
            "last_name": "Пользователь",
            "username": "user_updated",
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "user_updated")
        self.assertRedirects(response, reverse("users"))

    def test_superuser_cannot_update_annette(self):
        self.client.force_login(self.user2)
        url = reverse("user_update", kwargs={"pk": self.user1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_annette_delete_own_account(self):
        url = reverse("user_delete", kwargs={"pk": self.user1.pk})
        response = self.client.post(url, {"confirm": True}, follow=True)
        self.assertFalse(User.objects.filter(pk=self.user1.pk).exists())