from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Автоматически разрешает доступ к БД для всех тестов."""
    pass


@pytest.fixture
def logout_url():
    """URL страницы выхода."""
    return reverse('users:logout')


@pytest.fixture
def news():
    """Фикстура создаёт новость."""
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def author(django_user_model):
    """Фикстура создаёт автора комментария."""
    return django_user_model.objects.create(username='Лев Толстой')


@pytest.fixture
def reader(django_user_model):
    """Фикстура создаёт читателя."""
    return django_user_model.objects.create(username='Читатель простой')


@pytest.fixture
def author_client(author):
    """Клиент, залогиненный под автором."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    """Клиент, залогиненный под читателем."""
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def comment(news, author):
    """Фикстура создаёт комментарий от имени автора."""
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def news_bulk():
    """Фикстура создаёт пакет новостей с разными датами."""
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comments(news, author):
    """Фикстура создаёт 10 комментариев с разным временем."""
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def form_data():
    """Данные для POST-запроса при создании/редактировании комментария."""
    return {'text': 'Текст комментария'}


@pytest.fixture
def home_url():
    """URL главной страницы."""
    return reverse('news:home')


@pytest.fixture
def login_url():
    """URL страницы входа."""
    return reverse('users:login')


@pytest.fixture
def signup_url():
    """URL страницы регистрации."""
    return reverse('users:signup')


@pytest.fixture
def news_detail_url(news):
    """URL страницы отдельной новости."""
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def comment_edit_url(comment):
    """URL страницы редактирования комментария."""
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def comment_delete_url(comment):
    """URL страницы удаления комментария."""
    return reverse('news:delete', args=(comment.id,))
