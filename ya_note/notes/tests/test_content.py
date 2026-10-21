from notes.forms import NoteForm

from .base import BaseTest


class TestNotesList(BaseTest):
    """Тестируем страницу списка заметок."""

    def test_notes_list_for_different_users(self):
        """Список содержит только заметки текущего пользователя."""
        cases = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        for client, expected in cases:
            with self.subTest(client=client):
                response = client.get(self.list_url)
                object_list = response.context['object_list']
                self.assertEqual(self.note_author in object_list, expected)


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
