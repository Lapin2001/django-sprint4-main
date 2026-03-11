from django.urls import reverse_lazy

# Фикстуры для URL, которые ожидают тесты
PROFILE_EDIT_URL = '/users/profile/edit/'
PASSWORD_CHANGE_URL = '/users/password/change/'

# Именованные URL для использования в шаблонах
PROFILE_EDIT_NAME = 'users:profile_edit'
PASSWORD_CHANGE_NAME = 'users:password_change'

# URL для редиректов
PROFILE_URL = '/profile/{username}/'
LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'