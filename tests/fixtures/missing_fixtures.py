import pytest
from mixer.backend.django import Mixer
from blog.models import Post, Category, Location
import datetime
from django.utils import timezone

@pytest.fixture
def unpublished_posts_with_published_locations(
    mixer: Mixer, user, published_locations, published_category
):
    """Посты, снятые с публикации, но с опубликованными локациями"""
    return mixer.cycle(3).blend(
        'blog.Post',
        author=user,
        category=published_category,
        location=mixer.sequence(*published_locations),
        is_published=False,
    )

@pytest.fixture
def post_with_another_category(
    mixer: Mixer, user, published_location, published_category, another_category
):
    """Пост в другой категории"""
    return mixer.blend(
        'blog.Post',
        author=user,
        location=published_location,
        category=another_category,
        is_published=True,
    )

@pytest.fixture
def post_of_another_author(
    mixer: Mixer, another_user, published_location, published_category
):
    """Пост другого автора"""
    return mixer.blend(
        'blog.Post',
        author=another_user,
        location=published_location,
        category=published_category,
        is_published=True,
    )

@pytest.fixture
def posts_with_unpublished_category(
    mixer: Mixer, user, published_location, unpublished_category
):
    """Посты в категории, снятой с публикации"""
    return mixer.cycle(3).blend(
        'blog.Post',
        author=user,
        location=published_location,
        category=unpublished_category,
        is_published=True,
    )

@pytest.fixture
def future_posts(
    mixer: Mixer, user, published_location, published_category
):
    """Посты с датой публикации в будущем"""
    future_date = timezone.now() + datetime.timedelta(days=30)
    return mixer.cycle(3).blend(
        'blog.Post',
        author=user,
        location=published_location,
        category=published_category,
        is_published=True,
        pub_date=future_date,
    )

@pytest.fixture
def many_posts_with_published_locations(
    mixer: Mixer, user, published_locations, published_category
):
    """Много постов для тестирования пагинации"""
    return mixer.cycle(20).blend(
        'blog.Post',
        author=user,
        category=published_category,
        location=mixer.sequence(*published_locations),
        is_published=True,
    )

@pytest.fixture
def post_comment_context_form_item(
    mixer: Mixer, user, published_location, published_category
):
    """Фикстура для тестов комментариев"""
    from blog.forms import CommentForm
    post = mixer.blend(
        'blog.Post',
        author=user,
        location=published_location,
        category=published_category,
        is_published=True,
    )
    return ('comment_form', CommentForm)

@pytest.fixture
def create_post_context_form_item(
    mixer: Mixer, user
):
    """Фикстура для тестов создания поста"""
    from blog.forms import PostForm
    return ('form', PostForm)
