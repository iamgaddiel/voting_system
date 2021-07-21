from typing import Any, Dict, Optional
from django.db import models
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.contrib.auth.hashers import make_password

from polls.models import Polls
from core.models import CustomUser
from judges.models import JudgeProfile, JudgesPoll
from participants.models import ParticipantPolls, Participant

from admin_app.forms import UserCreationForm, PollsCreationForm




class AdminDashboard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['total_polls'] = Polls.objects.all().count()
        context['total_admins'] = CustomUser.objects.filter(is_admin=True).count()
        context['total_users'] = CustomUser.objects.all().count()
        context['total_participants'] = CustomUser.objects.filter(is_participant=True).count()
        context['total_judges'] = CustomUser.objects.filter(is_judge=True).count()
        return context

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

# ============================================[ Polls ] ========================================
class ListPoll(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/list_polls.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['polls'] = Polls.objects.all()
        context['participants_poll'] = ParticipantPolls.objects.all()
        context['judges_poll'] = JudgesPoll.objects.all()
        return context

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

class CreatePoll(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'admin/form.html'
    model = Polls
    form_class = PollsCreationForm
    success_url = reverse_lazy('admin_polls_list')

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['traceback_link'] = resolve_url('admin_user_list')
        context['form_title'] = 'Poll Creation'
        return context

class DeleteAllPolls(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        Polls.objects.all().delete()
        return JsonResponse({'data': 'deleted'}, status=200)

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

class DeleteSinglePoll(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            Polls.objects.get(id=kwargs.get('pk')).delete()
            return redirect('admin_polls_list')
        except Polls.DoesNotExist:
            return JsonResponse({"error": 'Polls does not exist'}, status=404)
        
    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

class UpdatePoll(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'admin/add_poll.html'
    model = Polls
    form_class = PollsCreationForm
    success_url = reverse_lazy('admin_polls_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Poll Update'
        return context

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

class GetPoll(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    template_name = "admin/get_polls.html"
    queryset = Polls.objects.all()
    context_object_name = "poll"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        current_poll = get_object_or_404(Polls, pk=self.kwargs.get('pk')) # get poll address from url parameter

        context['participants'] = ParticipantPolls.objects.filter(polls=current_poll)
        context['judges'] = JudgesPoll.objects.filter(polls=current_poll)
        context['account_type'] = 'admin'
        return context

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False


# ====================================== [ Judge ] ==========================================

class CreateJudge(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'admin/form.html'
    # model = JudgeProfile
    form_class = UserCreationForm
    success_url = reverse_lazy('admin_judges_list')


    def form_valid(self, form) -> HttpResponse:
        form.instance.is_judge = True
        form.instance.password = make_password(form.instance.password)
        form.save(commit=True)
        JudgeProfile.objects.create(user=form.instance)
        return redirect('admin_judges_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['traceback_link'] = resolve_url('admin_judges_list')
        context['form_title'] = 'Judge Creation'
        return context

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False


class DeleteJudge(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        judge = get_object_or_404(JudgeProfile, id=kwargs.get('id'))
        CustomUser.objects.get(id=judge.user.id).delete()
        return redirect('admin_judges_list')

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False   


class GetJudge(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/user_detail.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['object'] = judge = JudgeProfile.objects.get(id=kwargs.get('id'))
        context['object_polls'] = JudgesPoll.objects.filter(judge=judge)
        context['is_judge'] = True
        return context

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False


class ListJudges(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = JudgeProfile.objects.all()
    template_name = "admin/list_judges.html"
    context_object_name = "judges"
    ordering = ['-id']

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False


# ====================================== [ Participant ] ==========================================

class ListParticipants(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = Participant.objects.all()
    template_name = "admin/list_participants.html"
    context_object_name = "participants"

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

class DeleteParticipant(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        get_object_or_404(CustomUser, id=self.kwargs.get('id')).delete()
        return redirect('admin_participants_list')

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

class GetParticipant(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/user_detail.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['object'] = participant = Participant.objects.get(id=kwargs.get('id'))
        context['object_polls'] = ParticipantPolls.objects.filter(participant=participant)
        return context

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False


# ===================================== [Admin] ====================================
class CreateAdmin(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    queryset = CustomUser.objects.all()
    template_name = "admin/form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('admin_user_list')

    def form_valid(self, form) -> HttpResponse:
        form.instance.is_admin = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['traceback_link'] = resolve_url('admin_user_list')
        context['form_title'] = 'Admin Creation Form'
        return context

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

class DeleteAdmin(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        CustomUser.objects.get(id=kwargs.get('pk')).delete()
        return redirect('admin_user_list')

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

class UpdateAdmin(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pass

class GetAdmin(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    queryset = CustomUser.objects.all()
    template_name = "admin/user_detail.html"
    context_object_name = "admin"

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False

class ListAdmin(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = CustomUser.objects.filter(is_admin=True)
    template_name = "admin/list_admin.html"
    context_object_name = "admins"

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_admin:
            return True
        return False
