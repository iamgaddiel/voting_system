from django.db.models.base import Model
from django import forms
from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    password_2 = forms.CharField(
        min_length=8, 
    )
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name', 
            'last_name', 
            'password', 
            'password_2', 
            'email', 
            'account_type'
        ]
