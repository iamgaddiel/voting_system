import json
from typing import Any, Dict
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View

from judges.models import JudgeProfile, JudgesPoll
from participants.models import Participant, ParticipantPolls
from polls.models import Polls


class JudgesDashboard(LoginRequiredMixin, TemplateView):
    template_name = "participants/dashboard.html"

    def  get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        judge_profile = JudgeProfile.objects.get(user=self.request.user)
        
        context['polls'] = JudgesPoll.objects.filter(judge=judge_profile) # get all poll that partaining to this judge
        context['account_type'] = "judge"
        return context

class JudgePollDashboard(LoginRequiredMixin, TemplateView):
    template_name = "judges/judges_dashboard.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        poll_address = self.kwargs.get('poll_address') #get poll address from url parameter
        current_poll = get_object_or_404(Polls, address=poll_address) #get poll using it's address
        judge_profile = JudgeProfile.objects.get(user=self.request.user) # get judge profile instance
        all_participants = ParticipantPolls.objects.filter(polls=current_poll) # get all participants in the same poll
        all_judges = JudgesPoll.objects.filter(polls=current_poll)


        context['participants'] = all_participants
        context['polls'] = JudgesPoll.objects.filter(judge=judge_profile) # get all the polls this judge has joined
        context['poll_address'] = poll_address
        context['judges'] = all_judges
        # context['current_poll'] = ParticipantPolls.objects.get(
        #     participant=participant, 
        #     polls=current_poll
        # )
        return context


class JoinPoll(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            # get request data when using fetchAPI
            # decode request.body
            poll_address = json.loads(request.body.decode('utf-8')).get('pollAddress')
            judge = JudgeProfile.objects.get(user=request.user)
            polls = Polls.objects.get(address=poll_address)
            JudgesPoll.objects.get_or_create(polls=polls, judge=judge)

            return JsonResponse({"data": "You've joined successfully"})
        except Polls.DoesNotExist:
            return JsonResponse({'data': 'Poll not found'})

