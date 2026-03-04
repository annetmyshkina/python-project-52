from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from labels.models import Labels
from statuses.models import Statuses

from .models import Tasks


class TaskCRUDTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        cls.status = Statuses.objects.create(name="Test Status")

        cls.task = Tasks.objects.create(
            name="Test task",
            description="Description for first task",
            status=cls.status,
            author=cls.user,
            executor=cls.user,
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username="testuser", password="testpass123")

    def test_urls_resolve_and_return_ok(self):
        urls = [
            ("tasks", "tasks/tasks_list.html", None),
            ("task_create", "tasks/task_create.html", None),
            ("task_detail", "tasks/task_detail.html", self.task.pk),
            ("task_update", "tasks/task_update.html", self.task.pk),
            ("task_delete", "tasks/task_delete.html", self.task.pk),
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
            reverse("tasks"),
            reverse("task_create"),
            reverse("task_detail", kwargs={"pk": self.task.pk}),
            reverse("task_update", kwargs={"pk": self.task.pk}),
            reverse("task_delete", kwargs={"pk": self.task.pk}),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_create_post(self):
        url = reverse("task_create")
        response = self.client.post(
            url,
            {
                "name": "New task",
                "description": "New description for new task",
                "status": self.status.pk,
                "author": self.user.pk,
                "executor": self.user.pk,
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("tasks"))
        self.assertTrue(Tasks.objects.filter(name="New task").exists())

    def test_detail_get(self):
        url = reverse("task_detail", kwargs={"pk": self.task.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_detail.html")
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.status.name)

    def test_update_post(self):
        url = reverse("task_update", kwargs={"pk": self.task.pk})
        response = self.client.post(
            url,
            {
                "name": "Updated task",
                "description": "Update description for updated task",
                "status": self.status.pk,
                "author": self.user.pk,
                "executor": self.user.pk,
            },
            follow=True,
        )

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated task")
        self.assertEqual(
            self.task.description, "Update description for updated task"
        )
        self.assertRedirects(response, reverse("tasks"))

    def test_delete_post(self):
        task = Tasks.objects.create(
            name="Delete Me",
            description="Description for delete me",
            status=self.status,
            author=self.user,
            executor=self.user,
        )
        url = reverse("task_delete", kwargs={"pk": task.pk})

        self.client.post(url, follow=True)
        self.assertFalse(Tasks.objects.filter(pk=task.pk).exists())


class TaskFilterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        cls.status1 = Statuses.objects.create(name="Done")
        cls.status2 = Statuses.objects.create(name="In Progress")

        cls.label_critical = Labels.objects.create(name="Critical")
        cls.label_bug = Labels.objects.create(name="Bug")

        cls.task1 = Tasks.objects.create(
            name="Critical Task Done",
            status=cls.status1,
            author=cls.user,
        )
        cls.task1.labels.add(cls.label_critical)

        cls.task2 = Tasks.objects.create(
            name="In Progress Critical Task",
            status=cls.status2,
            author=cls.user,
            executor=cls.user,
        )
        cls.task2.labels.add(cls.label_critical)

        cls.task3 = Tasks.objects.create(
            name="Bug Task In Progress",
            status=cls.status2,
            author=cls.user,
        )
        cls.task3.labels.add(cls.label_bug)

    def setUp(self):
        self.client = Client()
        self.client.login(username="testuser", password="testpass123")

    def test_filter_by_status_done(self):
        url = f"{reverse('tasks')}?status={self.status1.pk}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Critical Task Done")
        self.assertNotContains(response, "In Progress Critical")
        self.assertNotContains(response, "Bug Task")

    def test_filter_by_status_in_progress(self):
        url = f"{reverse('tasks')}?status={self.status2.pk}"
        response = self.client.get(url)

        self.assertContains(response, "In Progress Critical Task")
        self.assertContains(response, "Bug Task In Progress")
        self.assertNotContains(response, "Critical Task Done")

    def test_filter_by_executor(self):
        url = f"{reverse('tasks')}?executor={self.user.pk}"
        response = self.client.get(url)

        self.assertContains(response, "In Progress Critical Task")
        self.assertNotContains(response, "Critical Task Done")

    def test_filter_by_label_critical(self):
        url = f"{reverse('tasks')}?label={self.label_critical.pk}"
        response = self.client.get(url)

        self.assertContains(response, "Critical Task Done")
        self.assertContains(response, "In Progress Critical Task")
        self.assertNotContains(response, "Bug Task In Progress")

    def test_filter_by_label_bug(self):
        url = f"{reverse('tasks')}?label={self.label_bug.pk}"
        response = self.client.get(url)

        self.assertContains(response, "Bug Task In Progress")
        self.assertNotContains(response, "Critical Task Done")
        self.assertNotContains(response, "In Progress Critical Task")

    def test_filter_combination_status_label(self):
        base_url = reverse("tasks")
        params = urlencode({
            "status": self.status2.pk,
            "label": self.label_critical.pk
        })
        url = f"{base_url}?{params}"
        response = self.client.get(url)

        self.assertContains(response, "In Progress Critical Task")
        self.assertNotContains(response, "Critical Task Done")
        self.assertNotContains(response, "Bug Task In Progress")

    def test_empty_filter(self):
        url = reverse("tasks")
        response = self.client.get(url)

        self.assertContains(response, "Critical Task Done")
        self.assertContains(response, "In Progress Critical Task")
        self.assertContains(response, "Bug Task In Progress")

    def test_filter_form_in_context(self):
        response = self.client.get(reverse("tasks"))
        self.assertIn("filter", response.context)
        self.assertTrue(hasattr(response.context["filter"], "form"))
