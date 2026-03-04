from django.urls import path
from . import views

app_name = 'users'

# Для auth/registration/ нужен пустой путь
urlpatterns = [
    path('', views.registration, name='registration'),  # для auth/registration/
    path('registration/', views.registration, name='registration'),  # для users/registration/
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('password/change/', views.password_change, name='password_change'),
]
