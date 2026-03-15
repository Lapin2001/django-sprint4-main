from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """CBV для страницы 'О проекте'."""

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """CBV для страницы 'Правила'."""

    template_name = 'pages/rules.html'


# Обработчики ошибок (остаются как FBV)
def page_not_found(request, exception=None):
    """Обработчик ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Обработчик ошибки 500."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=""):
    """Обработчик ошибки CSRF."""
    return render(request, 'pages/403csrf.html', status=403)
