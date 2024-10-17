from django import forms
from django.contrib.auth.forms import UserCreationForm
from app01.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(required=True, max_length=15)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user