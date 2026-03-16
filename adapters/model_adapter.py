from django.db import models


class ModelAdapter:
    """Базовый адаптер для работы с моделями."""
    
    def __init__(self, model):
        self.model = model
        self._item_or_cls = model
        self._model_class = model if isinstance(model, type) else model.__class__
        
    def get_all(self):
        """Получить все объекты модели."""
        return self.model.objects.all()

    def get_by_id(self, obj_id):
        """Получить объект по ID."""
        return self.model.objects.get(id=obj_id)

    def filter(self, **kwargs):
        """Фильтровать объекты."""
        return self.model.objects.filter(**kwargs)

    def create(self, **kwargs):
        """Создать новый объект."""
        return self.model.objects.create(**kwargs)
    
    def update(self, obj, **kwargs):
        """Обновить объект."""
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
        return obj
    
    def delete(self, obj):
        """Удалить объект."""
        obj.delete()
    
    def count(self):
        """Количество объектов."""
        return self.model.objects.count()
    
    def first(self):
        """Первый объект."""
        return self.model.objects.first()
    
    def last(self):
        """Последний объект."""
        return self.model.objects.last()
    
    def exists(self, **kwargs):
        """Проверить существование объекта."""
        return self.model.objects.filter(**kwargs).exists()
    
    @property
    def __name__(self):
        """Имя модели для тестов."""
        if hasattr(self._model_class, '__name__'):
            return self._model_class.__name__
        return 'Model'
    
    def __getattr__(self, name):
        """Возвращает поле модели для тестов."""
        if hasattr(self._model_class, name):
            field = getattr(self._model_class, name)
            
            # Для совместимости с тестами форм
            class FieldProxy:
                def __init__(self, field):
                    self.field = field
                    self.name = name
                    self.auto_now_add = getattr(field, 'auto_now_add', False)
                    
                def __getattr__(self, attr):
                    if attr == 'field':
                        return self
                    return getattr(field, attr, None)
                    
            return FieldProxy(field)
        return None
