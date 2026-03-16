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
