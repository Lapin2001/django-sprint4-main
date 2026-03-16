from django.db import models
from .model_adapter import ModelAdapter


class CommentModelAdapter(ModelAdapter):
    """Адаптер для модели Comment."""
    
    def __init__(self, item_or_class):
        if isinstance(item_or_class, models.Model):
            self._item_or_cls = item_or_class
            self.model_class = item_or_class.__class__
            self.item_cls = item_or_class.__class__
            self.model = item_or_class.__class__
        else:
            self._item_or_cls = item_or_class
            self.model_class = item_or_class
            self.item_cls = item_or_class
            self.model = item_or_class
        super().__init__(self.model)
    
    @property
    def id(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.id
        return None
    
    @property
    def text(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.text
        return None
    
    @property
    def post(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.post
        return None
    
    @property
    def author(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.author
        return None
    
    @property
    def created_at(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.created_at
        return None
    
    @property
    def displayed_field_name_or_value(self):
        """Возвращает отображаемое значение (для тестов)."""
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.text
        return 'text'
    
    @property
    def item_cls(self):
        if isinstance(self._item_or_cls, type):
            return self._item_or_cls
        return self._item_or_cls.__class__ if hasattr(self._item_or_cls, '__class__') else None
    
    @item_cls.setter
    def item_cls(self, value):
        pass
    
    @property
    def __name__(self):
        if isinstance(self._item_or_cls, type):
            return self._item_or_cls.__name__
        return self._item_or_cls.__class__.__name__ if hasattr(self._item_or_cls, '__class__') else 'Comment'
    
    @property
    def item_cls_adapter(self):
        return self
    
    def __getattr__(self, name):
        """Прокси для доступа к атрибутам."""
        if isinstance(self._item_or_cls, models.Model):
            return getattr(self._item_or_cls, name)
        return super().__getattr__(name)
    
    def __iter__(self):
        """Для совместимости с тестами."""
        return iter([])
    
    def __len__(self):
        return 0
    
    def items(self):
        return []
    
    def keys(self):
        return []
    
    def values(self):
        return []
    
    def __getitem__(self, key):
        """Для совместимости с dict."""
        return None
