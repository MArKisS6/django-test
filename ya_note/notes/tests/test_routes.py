from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    """Тестируем маршруты проекта."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='test-note',
            author=cls.author,
        )

        cls.home_url = reverse('notes:home')
        cls.login_url = reverse('users:login')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')
        cls.list_url = reverse('notes:list')
        cls.success_url = reverse('notes:success')
        cls.add_url = reverse('notes:add')
        cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))

        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

    def test_status_codes(self):
        """Проверяем статус-коды для разных URL, клиентов и методов."""
        cases = (
            (self.home_url, 'client', 'get', HTTPStatus.OK),
            (self.login_url, 'client', 'get', HTTPStatus.OK),
            (self.signup_url, 'client', 'get', HTTPStatus.OK),
            (self.logout_url, 'client', 'post', HTTPStatus.FOUND),
            (self.list_url, 'author_client', 'get', HTTPStatus.OK),
            (self.success_url, 'author_client', 'get', HTTPStatus.OK),
            (self.add_url, 'author_client', 'get', HTTPStatus.OK),
            (self.detail_url, 'author_client', 'get', HTTPStatus.OK),
            (self.edit_url, 'author_client', 'get', HTTPStatus.OK),
            (self.delete_url, 'author_client', 'get', HTTPStatus.OK),
            (self.detail_url, 'reader_client', 'get', HTTPStatus.NOT_FOUND),
            (self.edit_url, 'reader_client', 'get', HTTPStatus.NOT_FOUND),
            (self.delete_url, 'reader_client', 'get', HTTPStatus.NOT_FOUND),
        )
        for url, client_name, method, expected_status in cases:
            with self.subTest(url=url, client=client_name):
                client = getattr(self, client_name)
                response = getattr(client, method)(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_for_anonymous_client(self):
        """Аноним при попытке зайти на страницы заметок → на логин."""
        urls = (
            self.list_url,
            self.success_url,
            self.add_url,
            self.detail_url,
            self.edit_url,
            self.delete_url,
        )
        for url in urls:
            with self.subTest(url=url):
                expected_url = f'{self.login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, expected_url)
