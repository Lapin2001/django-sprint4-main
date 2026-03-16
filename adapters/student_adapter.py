from django.db import models
from .model_adapter import ModelAdapter


class StudentModelAdapter(ModelAdapter):
    """Адаптер для модели Student."""
    
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
    def displayed_field_name_or_value(self):
        """Возвращает отображаемое значение (для тестов)."""
        if isinstance(self._item_or_cls, models.Model):
            return str(self._item_or_cls)
        return 'student'
    
    @property
    def item_cls(self):
        return self._item_or_cls if not isinstance(self._item_or_cls, models.Model) else self._item_or_cls.__class__
    
    @item_cls.setter
    def item_cls(self, value):
        pass
    
    @property
    def __name__(self):
        return 'Student'
    
    @property
    def item_cls_adapter(self):
        return self
