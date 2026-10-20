# notes/tests/test_logic.py
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):
    """Тестируем создание заметки."""

    NOTE_TITLE = 'Заголовок заметки'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = 'test-note'

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('notes:add')
        cls.login_url = reverse('users:login')
        cls.success_url = reverse('notes:success')
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG,
        }
        cls.note = Note.objects.create(
            title='Первая заметка',
            text='Текст',
            slug=cls.NOTE_SLUG,
            author=cls.user,
        )

    def test_anonymous_user_cant_create_note(self):
        """Аноним не может создать заметку."""
        initial_count = Note.objects.count()
        response = self.client.post(self.url, data=self.form_data)
        expected_url = f'{self.login_url}?next={self.url}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), initial_count)

    def test_user_can_create_note(self):
        """Авторизованный пользователь может создать заметку."""
        Note.objects.all().delete()
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.user)

    def test_user_cant_use_duplicate_slug(self):
        """Нельзя создать заметку с неуникальным slug."""
        initial_count = Note.objects.count()
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        form = response.context['form']
        self.assertFormError(form, 'slug', self.NOTE_SLUG + WARNING)
        self.assertEqual(Note.objects.count(), initial_count)


class TestNoteEditDelete(TestCase):
    """Тестируем редактирование и удаление заметок."""

    NOTE_TITLE = 'Заголовок заметки'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = 'test-note'
    NEW_NOTE_TEXT = 'Обновлённый текст'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author,
        )
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.success_url = reverse('notes:success')
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT,
            'slug': cls.NOTE_SLUG,
        }

    def test_author_can_edit_note(self):
        """Автор может редактировать свою заметку."""
        response = self.author_client.post(
            self.edit_url, data=self.form_data
        )
        self.assertRedirects(response, self.success_url)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_from_db.title, self.form_data['title'])
        self.assertEqual(note_from_db.text, self.form_data['text'])
        self.assertEqual(note_from_db.slug, self.form_data['slug'])
        self.assertEqual(note_from_db.author, self.author)

    def test_user_cant_edit_note_of_another_user(self):
        """Чужой пользователь не может редактировать заметку."""
        response = self.reader_client.post(
            self.edit_url, data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.slug, self.note.slug)
        self.assertEqual(note_from_db.author, self.note.author)

    def test_author_can_delete_note(self):
        """Автор может удалить свою заметку."""
        initial_count = Note.objects.count()
        response = self.author_client.post(self.delete_url)
        self.assertRedirects(response, self.success_url)
        self.assertEqual(Note.objects.count(), initial_count - 1)

    def test_user_cant_delete_note_of_another_user(self):
        """Чужой пользователь не может удалить заметку."""
        initial_count = Note.objects.count()
        response = self.reader_client.post(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), initial_count)
