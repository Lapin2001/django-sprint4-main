from django.db import models

class SimplePostAdapter:
    """Упрощенный адаптер для теста."""
    
    def __init__(self, item_or_class):
        self.item_or_class = item_or_class
        self.model_class = item_or_class if isinstance(item_or_class, type) else item_or_class.__class__
        
    def __getattr__(self, name):
        """Возвращает прокси для поля."""
        if hasattr(self.model_class, name):
            field = getattr(self.model_class, name)
            
            class FieldWrapper:
                def __init__(self, field):
                    self.field = field
                    self.name = name
                    
                @property
                def field(self):
                    return self
                    
            return FieldWrapper(field)
        return None
