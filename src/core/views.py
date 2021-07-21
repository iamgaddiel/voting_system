from typing import Any, Dict
import socket
from django.contrib.auth.models import User
from django.contrib import messages
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, CreateView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from judges.models import JudgeProfile

from participants.models import Participant
from .models import CustomUser, TempAccessCodes
from .forms import UserCreationForm, VerificationForm
from core import utils


class Index(TemplateView):
    template_name = 'core/index.html'


class AdminDashboard(LoginRequiredMixin, TemplateView):
    pass


class CodeVerification(LoginRequiredMixin, View):
    template_name = "core/verify_code.html"
    context = {
        "form": VerificationForm()
    }

    def get(self, request, *args, **kwargs) -> HttpResponse:
        code = utils.get_random_text(10)
        message = f"Dear {request.user.username}\nThis is your verification code  \n{code}"
        # !delete current user code if found
        # !then create a new code for the user
        try:
            temp_code = TempAccessCodes.objects.filter(user=request.user)
            if temp_code.count() == 0:
                TempAccessCodes.objects.create(user=request.user, code=code)
            else:
                temp_code.first().delete()
                TempAccessCodes.objects.create(user=request.user, code=code)
            utils.send_mail("Verification Code", message, [request.user.username])
                
        #handles no internet connection
        except socket.gaierror:
            messages.warning(request, "No internet connection")
            return render(request, self.template_name, self.context)     

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        user_code = TempAccessCodes.objects.get(user=request.user)

        # !check if inputted code matches user code
        if user_code.code != request.POST.get('verification_code'):
            messages.info(request, "Invalid code")
            return render(request, self.template_name, self.context)

        return redirect('dispatcher')


class Dispacther(View):
    def get(self, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=self.request.user.id)
        print(user.is_participant, user.is_judge)
        url = ""
        if user.is_participant:
            url = "participant_dashboard"
        if user.is_judge:
            url = "judges_dashboard"
        if user.is_admin:
            url = "admin_dashboard"
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
            form.instance.is_participant = True
            form.save()
            user = CustomUser.objects.get(username=username)
            form.instance.is_judge = True
            JudgeProfile.objects.create(user=user)

        return redirect('login')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        account_type = self.kwargs.get('account_type')
        if account_type == "participant":
            context['account_type'] = "particiapant"
        elif account_type == "judge":
            context['account_type'] = "judge"
        return context
