from typing import Any, Dict, Optional
from django.db import models
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from core.forms import UserUpdateForm

from core.models import CustomUser
from judges.models import JudgeProfile, JudgesPoll
from participants.forms import ParticipantUpdateForm
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
        participant_poll = ParticipantPolls.objects.get(
            participant=participant, 
            polls=current_poll
        )
        judges = JudgesPoll.objects.filter(polls=current_poll)


        context['participants'] = all_participants
        context['polls'] = ParticipantPolls.objects.filter(participant=participant)
        context['current_poll'] = current_poll
        context['poll_address'] = poll_address
        context['judges'] = judges
        context['participant_poll'] = participant_poll
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

class ParticipantProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        template_name = "participants/profile_update.html"

        #! populate template form 
        context = {
            "main_form": UserUpdateForm(instance=request.user),
            "secondary_form": ParticipantUpdateForm(instance=request.user.participant),
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        user_update_form = UserUpdateForm(request.POST, request.user)
        judge_update_form =  ParticipantUpdateForm(request.POST, request.FILES, instance=request.user.participant)

        #! check if both submotted forms are valid
        if user_update_form.is_valid() and judge_update_form.is_valid():
            user_update_form.save()
            judge_update_form.save()
            return redirect("participant_profile")
        else:
            print(user_update_form.is_valid)
            print(judge_update_form.is_valid())
            return JsonResponse({"error": request.POST})

    def test_func(self) -> Optional[bool]:
        if not self.request.user.is_participant:
            return False
        return True

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