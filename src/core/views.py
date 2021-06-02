from typing import Any, Dict
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from judges.views import JudgesDashboard

from participants.models import Participant
from .models import CustomUser
from .forms import UserCreationForm


class Index(TemplateView):
    template_name = 'core/index.html'

class AdminDashboard(LoginRequiredMixin, TemplateView):
    pass

class Dispacther(View):
    def get(self, *args, **kwargs):
        logged_user = self.request.user
        url = ""
        if logged_user.is_participant:
            url = "participant_dashboard"
        if logged_user.is_judge:
            url = "judges_dashboard"
        return redirect(url)

class Regisration(CreateView):
    form_class = UserCreationForm
    models = CustomUser
    template_name = 'core/register.html'
    
    def form_valid(self, form) -> HttpResponse: 
        account_type = self.request.POST.get('account_type')
        username = form.instance.username

        if account_type == "participant":
            form.instance.is_participant = True
            form.save()
            user = CustomUser.objects.get(username=username)
            Participant.objects.create(user=user)
            
        if account_type == "judge":
            form.instance.is_judge = True
            form.save()
            user = CustomUser.objects.get(username=username)
            JudgesDashboard.objects.create(user=user)

        return redirect('login')
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        account_type = self.kwargs.get('account_type')
        if  account_type == "participant":
            context['account_type'] = "particiapant"
        elif account_type == "judge":
            context['account_type'] = "judge"
        return context

