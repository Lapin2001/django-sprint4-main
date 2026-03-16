import pytest
from adapters.comment import CommentModelAdapter
from adapters.post import PostModelAdapter
from adapters.user import UserModelAdapter

# Явно определяем фикстуры для адаптеров
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

# Алиасы для обратной совместимости
@pytest.fixture
def CommentModelAdapter(comment_model_adapter):
    return comment_model_adapter

@pytest.fixture
def PostModelAdapter(post_model_adapter):
    return post_model_adapter

@pytest.fixture
def UserModelAdapter(user_model_adapter):
    return user_model_adapter
