from django import forms
from django.db.models import fields
from .models import Participant


class ParticipantUpdateForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            "image",
            "stack"
        ]


