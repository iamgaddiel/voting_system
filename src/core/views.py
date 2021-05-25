from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import UserCreationForm


class Index(TemplateView):
    template_name = 'core/index.html'

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

class Regisration(CreateView):
    form_class = UserCreationForm
    models = CustomUser
    template_name = 'core/register.html'