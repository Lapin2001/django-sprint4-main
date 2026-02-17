"""Views for user authentication and profile management."""
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.shortcuts import redirect, render
from .forms import CustomUserChangeForm


def registration(request):
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(
                'blog:profile',
                username=user.username
            )
    else:
        form = UserCreationForm()

    return render(
        request,
        'registration/registration.html',
        {'form': form}
    )


@login_required
def profile_edit(request):
    """Редактирование профиля пользователя."""
    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect(
                'blog:profile',
                username=request.user.username
            )
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(
        request,
        'registration/profile_edit.html',
        {'form': form}
    )


@login_required
def password_change(request):
    """Изменение пароля."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(
                'blog:profile',
                username=request.user.username
            )
    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        'registration/password_change_form.html',
        {'form': form}
    )
