from django.test import Client, TestCase
from django.contrib.auth.models import User
from statuses.models import Statuses
from .models import Tasks
from django.urls import reverse


class TaskCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.status = Statuses.objects.create(name='Test Status')

        cls.task = Tasks.objects.create(
            name='Test task',
            description='Description for first task',
            status=cls.status,
            author=cls.user,
            executor=cls.user
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_urls_resolve_and_return_ok(self):
        urls = [
            ('tasks', 'tasks/tasks_list.html', None),
            ('task_create', 'tasks/task_create.html', None),
            ('task_detail', 'tasks/task_detail.html', self.task.pk),
            ('task_update', 'tasks/task_update.html', self.task.pk),
            ('task_delete', 'tasks/task_delete.html', self.task.pk)
        ]

        for url_name, template, pk in urls:
            if pk is None:
                url = reverse(url_name)
            else:
                url = reverse(url_name, kwargs={'pk': pk})

            with self.subTest(url_name=url_name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)


    def test_login_required(self):
        self.client.logout()
        urls = [
            reverse('tasks'),
            reverse('task_create'),
            reverse('task_detail', kwargs={'pk': self.task.pk}),
            reverse('task_update', kwargs={'pk': self.task.pk}),
            reverse('task_delete', kwargs={'pk': self.task.pk}),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f"{reverse('login')}?next={url}"
                )

    def test_create_post(self):
        url = reverse('task_create')
        response = self.client.post(
            url,
            {
                'name': 'New task',
                'description': 'New description for new task',
                'status': self.status.pk,
                'author': self.user.pk,
                'executor': self.user.pk
            }, follow=True)

        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Tasks.objects.filter(name='New task').exists())

    def test_detail_get(self):
        url = reverse('task_detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.status.name)

    def test_update_post(self):
        url = reverse('task_update', kwargs={'pk': self.task.pk})
        response = self.client.post(
            url,
            {
                'name': 'Updated task',
                'description': 'Update description for updated task',
                'status': self.status.pk,
                'author': self.user.pk,
                'executor': self.user.pk
            }, follow=True)

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated task')
        self.assertEqual(self.task.description, 'Update description for updated task')
        self.assertRedirects(response, reverse('tasks'))

    def test_delete_post(self):
        task = Tasks.objects.create(
            name='Delete Me',
            description='Description for delete me',
            status=self.status,
            author=self.user,
            executor=self.user
        )
        url = reverse('task_delete', kwargs={'pk': task.pk})

        self.client.post(url, follow=True)
        self.assertFalse(Tasks.objects.filter(pk=task.pk).exists())



