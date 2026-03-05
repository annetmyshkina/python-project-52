from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Statuses
from task_manager.tasks.models import Tasks

from .models import Labels


class LabelCRUDTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        cls.label = Labels.objects.create(name="Test label")

    def setUp(self):
        self.client = Client()
        self.client.login(username="testuser", password="testpass123")

    def test_urls_resolve_and_return_ok(self):
        urls = [
            ("labels", "labels/labels_list.html", None),
            ("label_create", "labels/label_create.html", None),
            ("label_update", "labels/label_update.html", self.label.pk),
            ("label_delete", "labels/label_delete.html", self.label.pk),
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
            reverse("labels"),
            reverse("label_create"),
            reverse("label_update", kwargs={"pk": self.label.pk}),
            reverse("label_delete", kwargs={"pk": self.label.pk}),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_create_post(self):
        url = reverse("label_create")
        response = self.client.post(url, {"name": "New label"}, follow=True)

        self.assertRedirects(response, reverse("labels"))
        self.assertTrue(Labels.objects.filter(name="New label").exists())

    def test_update_post(self):
        url = reverse("label_update", kwargs={"pk": self.label.pk})
        self.client.post(url, {"name": "Updated label"}, follow=True)

        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated label")

    def test_delete_post(self):
        label = Labels.objects.create(name="Delete Me")
        url = reverse("label_delete", kwargs={"pk": label.pk})

        self.client.post(url, follow=True)
        self.assertFalse(Labels.objects.filter(pk=label.pk).exists())

    def test_cannot_delete_label_with_tasks(self):

        status = Statuses.objects.create(name="Test")
        label = Labels.objects.create(name="Protected")
        task = Tasks.objects.create(name="T", status=status, author=self.user)
        task.labels.add(label)

        url = reverse("label_delete", kwargs={"pk": label.pk})
        response = self.client.post(url, follow=True)

        self.assertTrue(Labels.objects.filter(pk=label.pk).exists())

        messages_list = list(response.context["messages"])
        self.assertTrue(any("used in" in str(m.message) for m in messages_list))
