from django import forms

class PasswordResetForm(forms.Form):
    username = forms.CharField(label='Username')
    phone_number = forms.CharField(label='Phone Number')
    password = forms.CharField(widget=forms.PasswordInput)