from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from users.models import CustomUser


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control input-right', }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'type': 'password', 'class': 'form-control input-right'}))


class CustomUserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control input-right', }))
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control input-right', }))

    color = forms.CharField(label='Пользовательский цвет', initial='pink',
                            widget=forms.TextInput(attrs={'type': 'color', 'class': 'color-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'type': 'password', 'class': 'form-control input-right'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
        attrs={'type': 'password', 'class': 'form-control input-right'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'password1', 'password2', 'color',)

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

class UserUpdateForm(forms.ModelForm):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control input-right', }))

    color = forms.CharField(label='Пользовательский цвет', initial='pink',
                            widget=forms.TextInput(attrs={'type': 'color', 'class': 'color-input'}))

    class Meta:
        model = CustomUser
        fields = ('name', 'color')
