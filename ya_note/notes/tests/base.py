from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class BaseTest(TestCase):
    """Базовый класс с общими фикстурами и константами URL."""

    AUTHOR_SLUG = 'note-author'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')

        cls.note_author = Note.objects.create(
            title='Заметка автора',
            text='Текст заметки автора',
            slug=cls.AUTHOR_SLUG,
            author=cls.author,
        )

        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.home_url = reverse('notes:home')
        cls.login_url = reverse('users:login')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')
        cls.list_url = reverse('notes:list')
        cls.success_url = reverse('notes:success')
        cls.add_url = reverse('notes:add')
        cls.detail_author_url = reverse(
            'notes:detail', args=(cls.AUTHOR_SLUG,)
        )
        cls.edit_author_url = reverse(
            'notes:edit', args=(cls.AUTHOR_SLUG,)
        )
        cls.delete_author_url = reverse(
            'notes:delete', args=(cls.AUTHOR_SLUG,)
        )
