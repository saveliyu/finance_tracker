from django.contrib.auth.forms import AuthenticationForm
from django import forms


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control input-right', }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control input-right'}))


