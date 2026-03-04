from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Профиль пользователя."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField('Биография', max_length=500, blank=True)

    def __str__(self):
        return f'Профиль {self.user.username}'
