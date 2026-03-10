from django.contrib.auth import logout
from django.contrib.auth.views import LoginView

from .forms import CustomUserLoginForm
from django.shortcuts import redirect


class CustomUserLoginView(LoginView):
    form_class = CustomUserLoginForm
    template_name = 'users/login.html'
    success_url = '/'

def logout_view(request):
    logout(request)
    return redirect('/')