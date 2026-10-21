from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('home_url'),
        pytest.lazy_fixture('news_detail_url'),
        pytest.lazy_fixture('login_url'),
        pytest.lazy_fixture('signup_url'),
    ),
)
def test_pages_availability(client, url):
    """Проверяем доступность основных страниц для анонима."""
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'url, parametrized_client, method, expected_status',
    (
        (pytest.lazy_fixture('home_url'), 'client', 'get', HTTPStatus.OK),
        (pytest.lazy_fixture('news_detail_url'), 'client', 'get', HTTPStatus.OK),
        (pytest.lazy_fixture('login_url'), 'client', 'get', HTTPStatus.OK),
        (pytest.lazy_fixture('signup_url'), 'client', 'get', HTTPStatus.OK),
        (pytest.lazy_fixture('logout_url'), 'client', 'post', HTTPStatus.FOUND),
        (pytest.lazy_fixture('comment_edit_url'), 'author_client', 'get', HTTPStatus.OK),
        (pytest.lazy_fixture('comment_delete_url'), 'author_client', 'get', HTTPStatus.OK),
        (pytest.lazy_fixture('comment_edit_url'), 'reader_client', 'get', HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('comment_delete_url'), 'reader_client', 'get', HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('comment_edit_url'), 'client', 'get', HTTPStatus.FOUND),
        (pytest.lazy_fixture('comment_delete_url'), 'client', 'get', HTTPStatus.FOUND),
    ),
)
def test_status_codes(
    url, parametrized_client, method, expected_status, request
):
    """Проверяем соответствие статус-кодов ожидаемым."""
    client = request.getfixturevalue(parametrized_client)
    response = getattr(client, method)(url)
    assert response.status_code == expected_status
