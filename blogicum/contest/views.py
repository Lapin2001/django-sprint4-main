from django.shortcuts import render
from .forms import ContestForm


def contest_form(request):
    form = ContestForm(request.GET or None)

    context = {
        'form': form,
    }

    if request.method == 'GET' and request.GET:
        context['form_is_valid'] = form.is_valid()

    return render(request, 'contest/form.html', context)
