from http import HTTPStatus

import pytest
from django.urls import reverse


HOME_URL = reverse('news:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')


@pytest.fixture
def detail_url(news):
    """URL страницы новости."""
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def edit_url(comment):
    """URL редактирования комментария."""
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    """URL удаления комментария."""
    return reverse('news:delete', args=(comment.id,))


DETAIL_URL = pytest.lazy_fixture('detail_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')

CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
READER_CLIENT = pytest.lazy_fixture('reader_client')


@pytest.mark.parametrize(
    'url',
    (
        HOME_URL,
        DETAIL_URL,
        LOGIN_URL,
        SIGNUP_URL,
    ),
)
def test_pages_availability(client, url):
    """Проверяем доступность основных страниц для анонима."""
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'url, parametrized_client, method, expected_status',
    (
        (HOME_URL, CLIENT, 'get', HTTPStatus.OK),
        (DETAIL_URL, CLIENT, 'get', HTTPStatus.OK),
        (LOGIN_URL, CLIENT, 'get', HTTPStatus.OK),
        (SIGNUP_URL, CLIENT, 'get', HTTPStatus.OK),
        (LOGOUT_URL, CLIENT, 'post', HTTPStatus.OK),
        (EDIT_URL, AUTHOR_CLIENT, 'get', HTTPStatus.OK),
        (DELETE_URL, AUTHOR_CLIENT, 'get', HTTPStatus.OK),
        (EDIT_URL, READER_CLIENT, 'get', HTTPStatus.NOT_FOUND),
        (DELETE_URL, READER_CLIENT, 'get', HTTPStatus.NOT_FOUND),
        (EDIT_URL, CLIENT, 'get', HTTPStatus.FOUND),
        (DELETE_URL, CLIENT, 'get', HTTPStatus.FOUND),
    ),
)
def test_status_codes(url, parametrized_client, method, expected_status):
    """Проверяем соответствие статус-кодов ожидаемым."""
    response = getattr(parametrized_client, method)(url)
    assert response.status_code == expected_status
