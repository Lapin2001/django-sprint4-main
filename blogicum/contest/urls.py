from django.urls import path
from . import views

app_name = 'contest'

urlpatterns = [
    path('', views.contest_form, name='form'),
]
