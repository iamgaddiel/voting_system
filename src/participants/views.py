from typing import Any, Dict
from django.db import models
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from core.models import CustomUser
from polls.models import Polls
from .models import Participant, ParticipantPolls

import json


# utility function
def get_single_polls(poll_address):
    try:
        return Polls.objects.get(address=poll_address)
    except Polls.DoesNotExist:
        return None

class ParticipantDashboard(LoginRequiredMixin, TemplateView):
    template_name = "participants/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # todo: filter participants based on the selected poll
        context = super().get_context_data(**kwargs)
        participant = Participant.objects.get(user=self.request.user)
        
        context['polls'] = ParticipantPolls.objects.filter(participant=participant) # get all poll that belongs to this participant
        context['account_type'] = "participant"
        return context

class ParticipantPollsDashboard(LoginRequiredMixin, TemplateView):
    template_name = "participants/polls_dashboard.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        poll_address = kwargs.get('poll_address')
        current_poll = get_object_or_404(Polls, address=poll_address)
        participant = Participant.objects.get(user=self.request.user)
        all_participants = ParticipantPolls.objects.filter(polls=current_poll)


        context['participants'] = all_participants
        context['polls'] = ParticipantPolls.objects.filter(participant=participant)
        context['current_poll'] = ParticipantPolls.objects.get(
            participant=participant, 
            polls=current_poll
        )
        context['poll_address'] = poll_address
        return context

class ParticipantProfileDetail(LoginRequiredMixin, TemplateView):
    template_name = "participants/profile.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        participant = Participant.objects.get(user=self.request.user)
        all_participants = ParticipantPolls.objects.all()

        context['polls'] = ParticipantPolls.objects.filter(participant=participant)
        context['participants'] = all_participants
        return context

class JoinPoll(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            # get request data when using fetchAPI
            # decode request.body
            poll_address = json.loads(request.body.decode('utf-8')).get('pollAddress')
            participant = Participant.objects.get(user=request.user)
            polls = Polls.objects.get(address=poll_address)
            ParticipantPolls.objects.get_or_create(polls=polls, participant=participant)

            return JsonResponse({"data": "You've joined successfully"})
        except Polls.DoesNotExist:
            return JsonResponse({'data': 'Poll not found'})

class HandleProjectLinkUpload(View):
    def post(self, request, *args, **kwargs):
        # get parameters from fetchAPI
        project_link_address = json.loads(request.body.decode('utf-8')).get('projectLink')
        poll_address = json.loads(request.body.decode('utf-8')).get('pollAddress')

        polls = get_single_polls(poll_address)
        participant_poll = ParticipantPolls.objects.get(
            participant=request.user.participant, 
            polls=polls
        )

        participant_poll.project_link = project_link_address
        participant_poll.is_uploaded = True
        participant_poll.save()
        return JsonResponse({'data': 'uploaded successfully'})