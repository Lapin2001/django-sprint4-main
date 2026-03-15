from django.urls import path
from . import views

app_name = 'users'  # Это важно!

urlpatterns = [
    # Регистрация уже определена в главном urls.py как auth/registration/
    # Здесь дублируем для users/registration/
    path('registration/', views.registration, name='registration'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('password/change/', views.password_change, name='password_change'),
]
