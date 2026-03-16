from django.db import models


class ModelTestAdapter:
    """Адаптер для тестирования моделей."""
    
    def __init__(self, model_class):
        self.model_class = model_class
        self._model = model_class
    
    @property
    def __name__(self):
        return self.model_class.__name__
    
    def __getattr__(self, name):
        """Возвращает поле модели для тестов."""
        if hasattr(self.model_class, name):
            field = getattr(self.model_class, name)
            # Для совместимости с тестами
            if hasattr(field, 'field'):
                return field
            # Создаем прокси-объект
            class FieldProxy:
                def __init__(self, field):
                    self.field = field
                    self.auto_now_add = getattr(field, 'auto_now_add', False)
                    
            return FieldProxy(field)
        return None
