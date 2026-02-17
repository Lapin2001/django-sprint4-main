from django.urls import path
from . import views

app_name = 'users'  # Добавьте эту строку!

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('password-change/', views.password_change, name='password_change'),
]
