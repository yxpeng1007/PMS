from django import forms
from django.contrib.auth.forms import UserCreationForm
from app01.models import CustomUser
from django.db import models


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(required=True, max_length=15)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
        return user
