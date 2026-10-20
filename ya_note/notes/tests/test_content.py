from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class BaseTest(TestCase):
    """Базовый класс с общими фикстурами и константами URL."""

    AUTHOR_SLUG = 'note-author'
    READER_SLUG = 'note-reader'

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
        cls.note_reader = Note.objects.create(
            title='Заметка читателя',
            text='Текст заметки читателя',
            slug=cls.READER_SLUG,
            author=cls.reader,
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
        cls.detail_reader_url = reverse(
            'notes:detail', args=(cls.READER_SLUG,)
        )
        cls.edit_author_url = reverse(
            'notes:edit', args=(cls.AUTHOR_SLUG,)
        )
        cls.edit_reader_url = reverse(
            'notes:edit', args=(cls.READER_SLUG,)
        )
        cls.delete_author_url = reverse(
            'notes:delete', args=(cls.AUTHOR_SLUG,)
        )
        cls.delete_reader_url = reverse(
            'notes:delete', args=(cls.READER_SLUG,)
        )


class TestNotesList(BaseTest):
    """Тестируем страницу списка заметок."""

    def test_notes_list_for_different_users(self):
        """Список содержит только заметки текущего пользователя."""
        cases = (
            (self.author_client, self.note_author, True),
            (self.author_client, self.note_reader, False),
            (self.reader_client, self.note_reader, True),
            (self.reader_client, self.note_author, False),
        )
        for client, note, expected in cases:
            with self.subTest(client=client, note=note):
                response = client.get(self.list_url)
                object_list = response.context['object_list']
                self.assertEqual(note in object_list, expected)


class TestNoteForm(BaseTest):
    """Тестируем наличие формы на страницах создания и редактирования."""

    def test_pages_contains_form(self):
        """На страницах создания и редактирования есть форма."""
        urls = (self.add_url, self.edit_author_url)
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
