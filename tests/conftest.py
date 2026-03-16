import pytest
from typing import Any, List, Optional, Tuple, Union
from django import forms
from django.db import models
from django.http import HttpResponse
from django.test import Client
from http import HTTPStatus
import re
from dataclasses import dataclass


@dataclass
class KeyVal:
    key: str
    val: Any


@dataclass
class UrlRepr:
    """Представление URL."""
    name: str
    url: str


@dataclass
class TitledUrlRepr(UrlRepr):
    """Представление URL с заголовком."""
    title: str


N_PER_PAGE = 10


class _TestModelAttrs:
    """Класс для тестирования атрибутов модели."""
    
    def __init__(self, model):
        self.model = model


class ItemNotCreatedException(Exception):
    """Исключение, когда элемент не создан."""
    pass


class AuthenticatedEditException(Exception):
    """Исключение для ошибок редактирования аутентифицированных пользователей."""
    pass


def get_a_post_get_response_safely(
        user_client: Client, post_id: int, err_msg: Optional[str] = None,
        expected_status=HTTPStatus.OK
) -> HttpResponse:
    response = user_client.get(f"/posts/{post_id}/")
    if err_msg is not None:
        assert response.status_code == expected_status, err_msg
    return response


def get_create_a_post_get_response_safely(
        user_client: Client,
        expected_status=HTTPStatus.OK
) -> HttpResponse:
    response = user_client.get("/posts/create/")
    assert response.status_code == expected_status, (
        "Убедитесь, что страница создания поста загружается без ошибок."
    )
    return response


def _testget_context_item_by_class(
        context, cls: type, err_msg: str, inside_iter: bool = False
) -> KeyVal:
    """If `err_msg` is not empty, empty return value will
    produce an AssertionError with the `err_msg` error message"""

    def is_a_match(val: Any):
        if inside_iter:
            try:
                return isinstance(iter(val).__next__(), cls)
            except Exception:
                return False
        else:
            return isinstance(val, cls)

    matched_keyval: KeyVal = KeyVal(key=None, val=None)
    matched_keyvals: List[KeyVal] = []
    for key, val in dict(context).items():
        if is_a_match(val):
            matched_keyval = KeyVal(key, val)
            matched_keyvals.append(matched_keyval)
    if err_msg:
        assert len(matched_keyvals) == 1, err_msg

    return matched_keyval


def _testget_context_item_by_key(context, key: str, err_msg: str):
    """Получает элемент контекста по ключу."""
    for k, val in dict(context).items():
        if k == key:
            return KeyVal(k, val)
    if err_msg:
        assert False, err_msg
    return KeyVal(key=None, val=None)


def get_extra_urls(base_content: str, extra_content: str, ignore_urls=None):
    """Возвращает URL-ы, которые есть в extra_content, но нет в base_content."""
    if ignore_urls is None:
        ignore_urls = set()
    
    url_pattern = re.compile(r'href="([^"]+)"')
    base_urls = set(url_pattern.findall(base_content)) - ignore_urls
    extra_urls = set(url_pattern.findall(extra_content)) - ignore_urls
    
    return extra_urls - base_urls


def squash_code(code: str) -> str:
    """Удаляет пробелы и комментарии из кода."""
    lines = []
    for line in code.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            lines.append(line)
    return ''.join(lines)


def get_page_context_form(response, form_class, err_msg=None):
    """Получает форму из контекста страницы."""
    if hasattr(response, 'context'):
        context = response.context
        if context and 'form' in context:
            form = context['form']
            if isinstance(form, form_class):
                return form
    if err_msg:
        assert False, err_msg
    return None


def get_get_response_safely(
        user_client: Client, url: str, err_msg: Optional[str] = None,
        expected_status=HTTPStatus.OK
) -> HttpResponse:
    """Безопасно получает ответ по URL."""
    response = user_client.get(url)
    if err_msg is not None:
        assert response.status_code == expected_status, err_msg
    return response


def restore_cleaned_data(form):
    """Восстанавливает очищенные данные формы."""
    if hasattr(form, 'cleaned_data'):
        return form.cleaned_data
    return {}


# Фикстуры для адаптеров
from adapters.comment import CommentModelAdapter
from adapters.post import PostModelAdapter
from adapters.user import UserModelAdapter

@pytest.fixture
def comment_model_adapter():
    """Фикстура для адаптера комментариев."""
    return CommentModelAdapter

@pytest.fixture
def post_model_adapter():
    """Фикстура для адаптера постов."""
    return PostModelAdapter

@pytest.fixture
def user_model_adapter():
    """Фикстура для адаптера пользователей."""
    return UserModelAdapter

@pytest.fixture
def CommentModelAdapter(comment_model_adapter):
    return comment_model_adapter

@pytest.fixture
def PostModelAdapter(post_model_adapter):
    return post_model_adapter

@pytest.fixture
def UserModelAdapter(user_model_adapter):
    return user_model_adapter


# Стандартные фикстуры Django
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    """Фикстура для создания тестового пользователя."""
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def another_user(db):
    """Фикстура для создания другого тестового пользователя."""
    return User.objects.create_user(
        username='anotheruser',
        password='testpass123'
    )

@pytest.fixture
def user_client(user, client):
    """Клиент с авторизацией тестового пользователя."""
    client.force_login(user)
    return client

@pytest.fixture
def another_user_client(another_user, client):
    """Клиент с авторизацией другого пользователя."""
    client.force_login(another_user)
    return client

@pytest.fixture
def unlogged_client(client):
    """Неавторизованный клиент."""
    return client


# Фикстуры для контента
from blog.models import Post, Category, Location, Comment

@pytest.fixture
def published_category(db):
    """Опубликованная категория."""
    return Category.objects.create(
        title='Test Category',
        description='Test Description',
        slug='test-category',
        is_published=True
    )

@pytest.fixture
def published_location(db):
    """Опубликованное местоположение."""
    return Location.objects.create(
        name='Test Location',
        is_published=True
    )

@pytest.fixture
def post_with_published_location(db, user, published_category, published_location):
    """Пост с опубликованными категорией и местоположением."""
    return Post.objects.create(
        title='Test Post',
        text='Test text',
        author=user,
        category=published_category,
        location=published_location,
        pub_date='2024-01-01 12:00',
        is_published=True
    )

@pytest.fixture
def comment(db, user, post_with_published_location):
    """Комментарий к посту."""
    return Comment.objects.create(
        text='Test comment',
        author=user,
        post=post_with_published_location
    )

@pytest.fixture
def comment_to_a_post(db, another_user, post_with_published_location):
    """Комментарий другого пользователя к посту."""
    return Comment.objects.create(
        text='Another comment',
        author=another_user,
        post=post_with_published_location
    )

# Фикстуры для тестовых данных, использующие mixer
from mixer.backend.django import mixer as _mixer

@pytest.fixture
def mixer():
    """Фикстура для mixer."""
    return _mixer

@pytest.fixture
def post_comment_context_form_item(db, post_with_published_location, user_client):
    """Фикстура для формы комментария."""
    from blog.forms import CommentForm
    return KeyVal('form', CommentForm())

@pytest.fixture
def create_post_context_form_item(db, user_client):
    """Фикстура для формы создания поста."""
    from blog.forms import PostForm
    return KeyVal('form', PostForm())

@pytest.fixture
def future_posts(db, user, published_category, published_location):
    """Посты с будущей датой публикации."""
    from django.utils import timezone
    from datetime import timedelta
    
    posts = []
    for i in range(3):
        post = Post.objects.create(
            title=f'Future Post {i}',
            text=f'Future text {i}',
            author=user,
            category=published_category,
            location=published_location,
            pub_date=timezone.now() + timedelta(days=i+1),
            is_published=True
        )
        posts.append(post)
    return posts

@pytest.fixture
def unpublished_posts_with_published_locations(db, user, published_category, published_location):
    """Неопубликованные посты с опубликованными локациями."""
    posts = []
    for i in range(3):
        post = Post.objects.create(
            title=f'Unpublished Post {i}',
            text=f'Unpublished text {i}',
            author=user,
            category=published_category,
            location=published_location,
            pub_date='2024-01-01 12:00',
            is_published=False
        )
        posts.append(post)
    return posts

# Фикстуры для моделей
from blog.models import Post, Comment

@pytest.fixture
def PostModel():
    """Фикстура для модели Post."""
    return Post

@pytest.fixture
def CommentModel():
    """Фикстура для модели Comment."""
    return Comment

# Исправленные фикстуры для форм
@pytest.fixture
def post_comment_context_form_item(db, post_with_published_location, user_client):
    """Фикстура для формы комментария (возвращает кортеж)."""
    from blog.forms import CommentForm
    return ('form', CommentForm())

@pytest.fixture
def create_post_context_form_item(db, user_client):
    """Фикстура для формы создания поста (возвращает кортеж)."""
    from blog.forms import PostForm
    return ('form', PostForm())

# Недостающие фикстуры для тестов контента
@pytest.fixture
def post_with_another_category(db, user, published_location):
    """Пост в другой категории."""
    from blog.models import Category
    another_category = Category.objects.create(
        title='Another Category',
        description='Another Description',
        slug='another-category',
        is_published=True
    )
    return Post.objects.create(
        title='Post in Another Category',
        text='Text',
        author=user,
        category=another_category,
        location=published_location,
        pub_date='2024-01-01 12:00',
        is_published=True
    )

@pytest.fixture
def post_of_another_author(db, another_user, published_category, published_location):
    """Пост другого автора."""
    return Post.objects.create(
        title='Post by Another Author',
        text='Text',
        author=another_user,
        category=published_category,
        location=published_location,
        pub_date='2024-01-01 12:00',
        is_published=True
    )

@pytest.fixture
def posts_with_unpublished_category(db, user, published_location):
    """Посты с неопубликованной категорией."""
    from blog.models import Category
    unpublished_category = Category.objects.create(
        title='Unpublished Category',
        description='Description',
        slug='unpublished-category',
        is_published=False
    )
    posts = []
    for i in range(3):
        post = Post.objects.create(
            title=f'Post in Unpublished Category {i}',
            text=f'Text {i}',
            author=user,
            category=unpublished_category,
            location=published_location,
            pub_date='2024-01-01 12:00',
            is_published=True
        )
        posts.append(post)
    return posts

@pytest.fixture
def many_posts_with_published_locations(db, user, published_category, published_location):
    """Много постов с опубликованными локациями."""
    posts = []
    for i in range(15):
        post = Post.objects.create(
            title=f'Many Post {i}',
            text=f'Text {i}',
            author=user,
            category=published_category,
            location=published_location,
            pub_date=f'2024-01-{i+1:02d} 12:00',
            is_published=True
        )
        posts.append(post)
    return posts

# Фикстуры для тестеров контента
from test_content import ProfilePostContentTester, MainPostContentTester, CategoryPostContentTester

@pytest.fixture
def profile_content_tester(user, user_client, another_user_client):
    """Тестер для страницы профиля."""
    return ProfilePostContentTester(
        user=user,
        user_client=user_client,
        another_user_client=another_user_client
    )

@pytest.fixture
def main_content_tester(user_client, another_user_client):
    """Тестер для главной страницы."""
    return MainPostContentTester(
        user_client=user_client,
        another_user_client=another_user_client
    )

@pytest.fixture
def category_content_tester(published_category, user_client, another_user_client):
    """Тестер для страницы категории."""
    return CategoryPostContentTester(
        category_slug=published_category.slug,
        user_client=user_client,
        another_user_client=another_user_client
    )

# Фикстуры для тестеров контента с реальными URL-ами
@pytest.fixture
def profile_tester_with_url(user, user_client, another_user_client):
    """Тестер для страницы профиля с реальным URL."""
    from test_content import ProfilePostContentTester
    tester = ProfilePostContentTester(
        user=user,
        user_client=user_client,
        another_user_client=another_user_client
    )
    # Заменяем заглушку на реальный username
    tester.page_url.url = f"/profile/{user.username}/"
    return tester

@pytest.fixture
def category_tester_with_url(published_category, user_client, another_user_client):
    """Тестер для страницы категории с реальным URL."""
    from test_content import CategoryPostContentTester
    tester = CategoryPostContentTester(
        category_slug=published_category.slug,
        user_client=user_client,
        another_user_client=another_user_client
    )
    # Заменяем заглушку на реальный slug
    tester.page_url.url = f"/category/{published_category.slug}/"
    return tester
