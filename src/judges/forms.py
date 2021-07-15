from django import forms
from .models import JudgeProfile
from core.models import CustomUser


class JudgesUpdateForm(forms.ModelForm):
    class Meta:
        model = JudgeProfile
        exclude = ["user"]

