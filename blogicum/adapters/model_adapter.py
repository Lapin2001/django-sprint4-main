"""Адаптер для моделей Django."""


class ModelAdapter:
    """Адаптер для работы с моделями Django."""

    def __init__(self, model):
        self.model = model

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
