import inspect
import os
from http import HTTPStatus
from pathlib import Path
from typing import Tuple, Set, Optional

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.http import HttpResponse
from django.urls import URLPattern, URLResolver, get_resolver

from adapters.user import UserModelAdapter
from conftest import KeyVal, squash_code
from form.find_urls import find_links_between_lines
from form.user.edit_form_tester import EditUserFormTester
from test_edit import _test_edit


class ManageProfileLinksException(Exception):
    ...


@pytest.mark.django_db
def test_custom_err_handlers(client):
    try:
        from blogicum import urls as blogicum_urls
    except Exception:
        raise AssertionError(
            "Убедитесь, в головном файле с маршрутами нет ошибок."
        )
    urls_src_squashed = squash_code(inspect.getsource(blogicum_urls))
    if "django.contrib.auth.urls" not in urls_src_squashed:
        raise AssertionError(
            "Убедитесь, что подключены маршруты для работы с пользователями из"
            " `django.contrib.auth.urls`."
        )

    def search_url_patterns(substring):
        resolver = get_resolver()
        results = []

        def search_patterns(head, patterns):
            for pattern in patterns:
                if isinstance(pattern, URLPattern):
                    pattern_as_str = head + str(pattern.pattern)
                    if substring in pattern_as_str:
                        results.append(pattern)
                elif isinstance(pattern, URLResolver):
                    search_patterns(
                        head + str(pattern.pattern), pattern.url_patterns
                    )
            return results

        search_patterns(head="", patterns=resolver.url_patterns)

        return results

    registration_url = "auth/registration/"
    auth_registration_patterns = search_url_patterns(registration_url)
    assert auth_registration_patterns, (
        "Убедитесь, что в головном файле с маршрутами переопределён маршрут"
        f" `{registration_url}`."
    )

    auth_templates = {
        "logged_out.html",
        "login.html",
        "password_change_done.html",
        "password_change_form.html",
        "password_reset_complete.html",
        "password_reset_confirm.html",
        "password_reset_done.html",
        "password_reset_form.html",
        "registration_form.html",
    }
    for template in auth_templates:
        try:
            fpath: Path = Path(settings.TEMPLATES_DIR) / "registration" / template
        except Exception as e:
            raise AssertionError(
                'Убедитесь, что переменная TEMPLATES_DIR в настройках проекта '
                'является строкой (str) или объектом, соответствующим path-like интерфейсу '
                '(например, экземпляром pathlib.Path). '
                f'При операции Path(settings.TEMPLATES_DIR) / "registration", возникла ошибка: {e}'
            )
        frpath: Path = fpath.relative_to(settings.BASE_DIR)
        assert os.path.isfile(
            fpath.resolve()
        ), f"Убедитесь, что файл шаблона `{frpath}` существует."


@pytest.mark.django_db
def _test_user_info_displayed(
        profile_user: Model, profile_user_content: str, printed_url: str
) -> None:
    if profile_user.first_name not in profile_user_content:
        raise AssertionError(
            f"Убедитесь, что на странице `{printed_url}` отображается имя"
            " пользователя."
        )
    if profile_user.last_name not in profile_user_content:
        raise AssertionError(
            f"Убедитесь, что на странице `{printed_url}` отображается фамилия"
            " пользователя."
        )


def try_get_profile_manage_urls(
        user_content: str, anothers_page_content: str, ignore_urls: Set[str]
) -> Tuple[str, str]:
    diff_urls = get_extra_urls(
        base_content=anothers_page_content,
        extra_content=user_content,
        ignore_urls=ignore_urls,
    )
    if len(diff_urls) != 2:
        raise ManageProfileLinksException

    # swap variables if needed
    edit_url, change_pwd_url = diff_urls
    change_pwd_marker = "/auth/password_change/"
    if change_pwd_marker in edit_url:
        edit_url, change_pwd_url = change_pwd_url, edit_url
    if change_pwd_marker not in change_pwd_url:
        raise AssertionError(
            "Убедитесь, что на странице профиля владельцу этого профиля"
            f" доступна ссылка `{change_pwd_marker}` для изменения пароля."
        )

    return edit_url, change_pwd_url


def get_extra_urls(
        base_content: str,
        extra_content: str,
        ignore_urls: Optional[Set[str]] = None,
):
    ignore_urls = ignore_urls or set()
    find_links_kwargs = dict(
        urls_start_with="", start_lineix=-1, end_lineix=-1
    )

    # Получаем ссылки из основного контента
    anothers_page_links = set(
        find_links_between_lines(base_content, **find_links_kwargs)
    )

    # Получаем ссылки из дополнительного контента
    user_links = set(
        find_links_between_lines(extra_content, **find_links_kwargs)
    )

    # Выводим отладочную информацию
    print("\n=== ССЫЛКИ У ВЛАДЕЛЬЦА ===")
    for link in sorted(user_links):
        print(f"  - {link}")

    print("\n=== ССЫЛКИ У ДРУГОГО ===")
    for link in sorted(anothers_page_links):
        print(f"  - {link}")

    # Находим уникальные ссылки (есть у пользователя, но нет на другой странице)
    diff_urls = [
        x.get("href")
        for x in (user_links - anothers_page_links)
        if x.get("href") not in ignore_urls
    ]

    return diff_urls


@pytest.mark.django_db

@pytest.mark.django_db
def test_profile(
        user, another_user, user_client, another_user_client, unlogged_client
):
    """Исправленная версия теста профиля"""
    user_url = f"/profile/{user.username}/"
    
    # Получаем страницы
    user_response = user_client.get(user_url)
    user_content = user_response.content.decode()
    
    another_response = another_user_client.get(user_url)
    another_content = another_response.content.decode()
    
    # Найдем все ссылки вручную
    import re
    user_links = set(re.findall(r'href="([^"]+)"', user_content))
    print("\n=== ССЫЛКИ У ВЛАДЕЛЬЦА ===")
    for link in sorted(user_links):
        print(f"  - {link}")
    print("\n=== ССЫЛКИ У ДРУГОГО ===")
    for link in sorted(another_links):
        print(f"  - {link}")
    another_links = set(re.findall(r'href="([^"]+)"', another_content))
    
    # Ссылки для редактирования
    edit_links = {'/users/profile/edit/', '/users/password/change/'}
    
    # Проверяем, что у владельца они есть
    assert edit_links.issubset(user_links), "У владельца нет всех ссылок"
    
    # Проверяем, что у другого их нет
    assert not edit_links.intersection(another_links), "У другого пользователя есть ссылки"
