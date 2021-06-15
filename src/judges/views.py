import json
from typing import Any, Dict, Optional
from django.db import models
from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import View

from judges.models import JudgeProfile, JudgesPoll
from participants.models import Participant, ParticipantPolls
from polls.models import Polls
from core.models import CustomUser


class JudgesDashboardIndex(LoginRequiredMixin, TemplateView):
    template_name = "participants/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        judge_profile = JudgeProfile.objects.get(user=self.request.user)

        # get all poll that partaining to this judge
        context['polls'] = JudgesPoll.objects.filter(judge=judge_profile)
        context['account_type'] = "judge"
        return context


class JudgePollDashboard(LoginRequiredMixin, TemplateView):
    template_name = "judges/judges_dashboard.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        poll_address = self.kwargs.get('poll_address') # get poll address from url parameter
        current_poll = get_object_or_404(Polls, address=poll_address) 
        judge_profile = JudgeProfile.objects.get(user=self.request.user)
        all_poll_participants = ParticipantPolls.objects.filter(polls=current_poll)
        all_poll_judges = JudgesPoll.objects.filter(polls=current_poll)
        is_voted = JudgesPoll.objects.get(polls=current_poll, judge=judge_profile).is_voted

        context['participants'] = all_poll_participants
        context['polls'] = JudgesPoll.objects.filter(judge=judge_profile)  # get all the polls joined by a judge
        context['poll_address'] = poll_address
        context['judges'] = all_poll_judges
        context['account_type'] = 'judge'
        context['judge_status'] = self.request.user.is_judge
        context['is_voted'] = is_voted
        return context


class JoinPoll(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            # get request data when using fetchAPI
            # decode request.body
            poll_address = json.loads(
                request.body.decode('utf-8')).get('pollAddress')
            judge = JudgeProfile.objects.get(user=request.user)
            polls = Polls.objects.get(address=poll_address)
            JudgesPoll.objects.get_or_create(polls=polls, judge=judge)

            return JsonResponse({"data": "You've joined successfully"})
        except Polls.DoesNotExist:
            return JsonResponse({'data': 'Poll not found'})


class GetParticipantDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, **kwargs: Any) -> Dict[str, Any]:
        voted: bool = False
        voted_participant = False

        # get a participant with a user id
        get_participant = get_object_or_404(
            Participant, user=CustomUser.objects.get(id=kwargs.get('id')))
        poll = get_object_or_404(Polls, address=kwargs.get('poll_address'))  # get a single poll
        participant_poll = get_object_or_404(  # get a participant poll
            ParticipantPolls,
            polls=poll,
            participant=get_participant
        )
        judge_profile = JudgeProfile.objects.get(user=request.user.id)
        try:
            # check if judge has voted for this participant
            judge_poll = JudgesPoll.objects.get(
                voted_participant=participant_poll,
                judge=judge_profile,
                polls=poll
            )
            if judge_poll is not None:
                voted = True
                voted_participant = True
        except JudgesPoll.DoesNotExist:
            pass

        response = {
            "first_name": participant_poll.participant.user.first_name,
            "last_name": participant_poll.participant.user.last_name,
            "email": participant_poll.participant.user.email,
            "stack": participant_poll.participant.stack,
            "project_link": participant_poll.project_link,
            "participant_id": get_participant.id,
            "voted": voted,
            'voted_participant': voted_participant,
        }
        return JsonResponse({"data": response})

    def test_func(self) -> Optional[bool]:
        if not self.request.user.is_judge:
            return False
        return True


class VoteParticipant(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        _, poll_address, participant_id, judge_status, rating = json.loads(
            request.body.decode('utf-8')).values()
        judge_profile = JudgeProfile.objects.get(user=request.user.id)
        participant_poll = ParticipantPolls.objects.get(
            participant=participant_id)
        try:
            # check if judge has voted for a participant
            participant_poll = JudgesPoll.objects.get(
                polls=Polls.objects.get(address=poll_address),
                voted_participant=participant_poll,
                judge=judge_profile
            )
            if participant_poll is not None:
                return JsonResponse({'error': "you've voted"})

        except JudgesPoll.DoesNotExist:
            participant_poll.vote_count += 1
            participant_poll.total_rating += rating
            participant_poll.number_of_votes += 1
            participant_poll.save()
            judge_poll = JudgesPoll.objects.get(judge=judge_profile)
            judge_poll.rating = rating
            judge_poll.voted_participant = participant_poll
            judge_poll.is_voted = True
            judge_poll.save()

        return JsonResponse({'data': 'voted'})

    def test_func(self) -> Optional[bool]:
        user_is_judge = json.loads(
            self.request.body.decode('utf-8')).get('judgeStatus')
        if user_is_judge:
            return True
        return False


class GetRanking(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            poll_address = kwargs.get('address')
            poll = Polls.objects.get(address=poll_address)
            poll_judges = JudgesPoll.objects.filter(polls=poll)
            all_poll_participants = ParticipantPolls.objects.filter(polls=poll).order_by('-total_rating')
            polls_detail: list = [] # rating detail
            
            for participant_poll in all_poll_participants:
                for judge in poll_judges:
                    if judge.voted_participant == participant_poll:
                        rating_details: dict = {
                            'username' : participant_poll.participant.user.username,
                            'first_name': participant_poll.participant.user.first_name,
                            'last_name': participant_poll.participant.user.last_name,
                            'average_rating': participant_poll.get_avarage_rating()
                        }
                        polls_detail.append(rating_details)
            
            return JsonResponse({
                'data': {
                    'poll_details': polls_detail
                }
            })
        except ZeroDivisionError as zd_err:
            return JsonResponse({'error': str(zd_err)}, safe=False, status=403)

    def test_func(self) -> Optional[bool]:
        user = self.request.user
        if user.is_anonymous:
            return False
        else:
            if (not user.is_participant) and (not user.is_judge):
                return False
        return True
