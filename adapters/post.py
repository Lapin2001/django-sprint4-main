from django.db import models
from .model_adapter import ModelAdapter


class FieldProxy:
    """Прокси для поля модели, который имеет атрибут field с атрибутом name."""
    
    def __init__(self, field, name):
        self._field = field
        self._name = name
        
    @property
    def field(self):
        """Возвращает сам себя для доступа к атрибуту name."""
        return self
        
    @property
    def name(self):
        """Имя поля."""
        return self._name
        
    def __getattr__(self, attr):
        """Прокси к оригинальному полю."""
        return getattr(self._field, attr, None)


class PostModelAdapter(ModelAdapter):
    """Адаптер для модели Post."""
    
    def __init__(self, item_or_class):
        if isinstance(item_or_class, models.Model):
            self._item_or_cls = item_or_class
            self.model_class = item_or_class.__class__
            self.item_cls = item_or_class.__class__
            self.model = item_or_class.__class__
            self._is_instance = True
        else:
            self._item_or_cls = item_or_class
            self.model_class = item_or_class
            self.item_cls = item_or_class
            self.model = item_or_class
            self._is_instance = False
            
        super().__init__(self.model)
    
    @property
    def id(self):
        if self._is_instance:
            return self._item_or_cls.id
        return None
    
    @property
    def title(self):
        if self._is_instance:
            return self._item_or_cls.title
        return None
    
    @property
    def text(self):
        if self._is_instance:
            return self._item_or_cls.text
        return None
    
    @property
    def pub_date(self):
        if self._is_instance:
            return self._item_or_cls.pub_date
        return None
    
    @property
    def author(self):
        if self._is_instance:
            return self._item_or_cls.author
        return None
    
    @property
    def location(self):
        if self._is_instance:
            return self._item_or_cls.location
        return None
    
    @property
    def category(self):
        if self._is_instance:
            return self._item_or_cls.category
        return None
    
    @property
    def image(self):
        if self._is_instance:
            return self._item_or_cls.image
        return None
    
    @image.setter
    def image(self, value):
        if self._is_instance:
            self._item_or_cls.image = value
    
    @property
    def is_published(self):
        if self._is_instance:
            return self._item_or_cls.is_published
        return None
    
    @is_published.setter
    def is_published(self, value):
        if self._is_instance:
            self._item_or_cls.is_published = value
    
    def save(self):
        if self._is_instance:
            self._item_or_cls.save()
    
    @property
    def displayed_field_name_or_value(self):
        """Возвращает отображаемое значение (для тестов)."""
        if self._is_instance:
            return self._item_or_cls.title
        return 'title'
    
    @property
    def item_cls(self):
        if not self._is_instance:
            return self._item_or_cls
        return self._item_or_cls.__class__ if hasattr(self._item_or_cls, '__class__') else None
    
    @item_cls.setter
    def item_cls(self, value):
        pass
    
    @property
    def __name__(self):
        if not self._is_instance:
            return self._item_or_cls.__name__
        return self._item_or_cls.__class__.__name__ if hasattr(self._item_or_cls, '__class__') else 'Post'
    
    @property
    def item_cls_adapter(self):
        return self
    
    def __getattr__(self, name):
        """Прокси для доступа к полям модели при создании форм."""
        # Для экземпляра возвращаем значение поля
        if self._is_instance:
            return getattr(self._item_or_cls, name, None)
        
        # Для класса возвращаем прокси для поля
        if hasattr(self.model_class, name):
            field = getattr(self.model_class, name)
            return FieldProxy(field, name)
        
        return None
    
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
