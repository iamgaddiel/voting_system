from django.db.models.base import Model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import widgets
from .models import CustomUser


class UserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name', 
            'last_name', 
            'email', 
            'dob',
            'gender'
        ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name', 
            'last_name', 
            'email', 
        ]
