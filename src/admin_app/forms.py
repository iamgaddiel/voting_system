from typing import Any
from django import forms
from django.db.models import fields
from django.forms import widgets
from core.models import CustomUser
from polls.models import Polls



class PollsCreationForm(forms.ModelForm):
    class Meta:
        model = Polls
        exclude = ['address']

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'dob']
        widgets = {
            'email': widgets.TextInput(attrs={
                'type': 'email',
                'placeholder': 'example@example.com'
            }),
            'password': widgets.PasswordInput(attrs={
                'type': 'password',
                'placeholder': '!23!@kd#@k'
            }),
            'dob': widgets.DateInput(attrs={'type': 'date'}),
        }

