from django.db import models


class ModelAdapter:
    """Базовый адаптер для работы с моделями."""
    
    def __init__(self, model_class):
        self.model_class = model_class
        self._item_or_cls = model_class
        
    def get_all(self):
        return self.model_class.objects.all()
    
    def get_by_id(self, obj_id):
        return self.model_class.objects.get(id=obj_id)
    
    def filter(self, **kwargs):
        return self.model_class.objects.filter(**kwargs)
    
    def create(self, **kwargs):
        return self.model_class.objects.create(**kwargs)
    
    def update(self, obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
        return obj
    
    def delete(self, obj):
        obj.delete()
    
    def count(self):
        return self.model_class.objects.count()
    
    def first(self):
        return self.model_class.objects.first()
    
    def last(self):
        return self.model_class.objects.last()
    
    def exists(self, **kwargs):
        return self.model_class.objects.filter(**kwargs).exists()


class PostModelAdapter(ModelAdapter):
    """Адаптер для модели Post."""
    
    def __init__(self, item_or_class):
        if isinstance(item_or_class, models.Model):
            self._item_or_cls = item_or_class
            self.model_class = item_or_class.__class__
        else:
            self._item_or_cls = item_or_class
            self.model_class = item_or_class
        super().__init__(self.model_class)
    
    @property
    def id(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.id
        return None
    
    @property
    def title(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.title
        return None
    
    @property
    def text(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.text
        return None
    
    @property
    def pub_date(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.pub_date
        return None
    
    @property
    def author(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.author
        return None
    
    @property
    def location(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.location
        return None
    
    @property
    def category(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.category
        return None
    
    @property
    def image(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.image
        return None
    
    @property
    def is_published(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.is_published
        return None
    
    @is_published.setter
    def is_published(self, value):
        if isinstance(self._item_or_cls, models.Model):
            self._item_or_cls.is_published = value
    
    def save(self):
        if isinstance(self._item_or_cls, models.Model):
            self._item_or_cls.save()
    
    @property
    def displayed_field_name_or_value(self):
        """Возвращает отображаемое значение (для тестов)."""
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.title
        return 'title'


class UserModelAdapter(ModelAdapter):
    """Адаптер для модели User."""
    
    def __init__(self, item_or_class):
        if isinstance(item_or_class, models.Model):
            self._item_or_cls = item_or_class
            self.model_class = item_or_class.__class__
        else:
            self._item_or_cls = item_or_class
            self.model_class = item_or_class
        super().__init__(self.model_class)
    
    @property
    def id(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.id
        return None
    
    @property
    def username(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.username
        return None
    
    @property
    def first_name(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.first_name
        return None
    
    @property
    def last_name(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.last_name
        return None
    
    @property
    def email(self):
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.email
        return None
    
    @property
    def displayed_field_name_or_value(self):
        """Возвращает отображаемое значение (для тестов)."""
        if isinstance(self._item_or_cls, models.Model):
            return self._item_or_cls.username
        return 'username'


class CommentModelAdapter(ModelAdapter):
    """Адаптер для модели Comment."""
    
    def __init__(self, item_or_class):
        if isinstance(item_or_class, models.Model):
            self._item_or_cls = item_or_class
            self.model_class = item_or_class.__class__
        else:
            self._item_or_cls = item_or_class
            self.model_class = item_or_class
        super().__init__(self.model_class)
    
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
