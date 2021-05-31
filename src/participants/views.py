from typing import Any, Dict
from django.db import models
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from core.models import CustomUser
from polls.models import Polls
from .models import Participant


class ParticipantDashboard(LoginRequiredMixin, TemplateView):
    template_name = "participants/dashboard.html"

class ParticipantProfileDetail(LoginRequiredMixin, TemplateView):
    template_name = "participants/profile.html"

class JoinPoll(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            polls = Polls.objects.get(title=request.POST.get('poll'))
            
        except Polls.DoesNotExist:
            return 
