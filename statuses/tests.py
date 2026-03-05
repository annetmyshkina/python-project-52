from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Statuses


class StatusCRUDTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        cls.status = Statuses.objects.create(name="Test status")

    def setUp(self):
        self.client = Client()
        self.client.login(username="testuser", password="testpass123")

    def test_urls_resolve_and_return_ok(self):
        urls = [
            ("statuses", "statuses/statuses_list.html", None),
            ("status_create", "statuses/status_create.html", None),
            ("status_update", "statuses/status_update.html", self.status.pk),
            ("status_delete", "statuses/status_delete.html", self.status.pk),
        ]

        for url_name, template, pk in urls:
            if pk is None:
                url = reverse(url_name)
            else:
                url = reverse(url_name, kwargs={"pk": pk})

            with self.subTest(url_name=url_name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    def test_login_required(self):
        self.client.logout()
        urls = [
            reverse("statuses"),
            reverse("status_create"),
            reverse("status_update", kwargs={"pk": self.status.pk}),
            reverse("status_delete", kwargs={"pk": self.status.pk}),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_create_post(self):
        url = reverse("status_create")
        response = self.client.post(url, {"name": "New status"}, follow=True)

        self.assertRedirects(response, reverse("statuses"))
        self.assertTrue(Statuses.objects.filter(name="New status").exists())

    def test_update_post(self):
        url = reverse("status_update", kwargs={"pk": self.status.pk})
        self.client.post(url, {"name": "Updated status"}, follow=True)

        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated status")

    def test_delete_post(self):
        status = Statuses.objects.create(name="Delete Me")
        url = reverse("status_delete", kwargs={"pk": status.pk})

        self.client.post(url, follow=True)
        self.assertFalse(Statuses.objects.filter(pk=status.pk).exists())

    def test_cannot_delete_status_with_tasks(self):
        from tasks.models import Tasks

        status = Statuses.objects.create(name="Protected")
        Tasks.objects.create(name="T", status=status, author=self.user)

        url = reverse("status_delete", kwargs={"pk": status.pk})
        response = self.client.post(url, follow=True)

        self.assertTrue(Statuses.objects.filter(pk=status.pk).exists())

        messages = list(response.context["messages"])
        self.assertTrue(
            any(
                'Status "Protected" used in 1 tasks' in str(m.message)
                for m in messages
            )
        )
