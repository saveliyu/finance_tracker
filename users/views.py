from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView, DetailView

from .forms import CustomUserLoginForm, CustomUserRegisterForm, UserUpdateForm
from django.shortcuts import redirect

from .models import CustomUser

from users.utils import *

from base.models import Purchase


def user_logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='users:login')
def change_data(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    return redirect('users:profile')


class CustomUserLoginView(LoginView):
    form_class = CustomUserLoginForm
    template_name = 'users/login.html'
    success_url = '/'


class CustomUserRegisterView(CreateView):
    form_class = CustomUserRegisterForm
    template_name = 'users/register.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        user_purchases = Purchase.objects.filter(user=self.request.user)
        profile_data = get_profile_stats(user_purchases)
        streak = get_streak(user_purchases)
        activity = get_activity_days(user_purchases)
        top_category, top_category_proportion = get_top_category(user_purchases)
        context = {
            'profile_data': profile_data,

            # Стрик
            "streak": streak,

            # Тепловая карта
            "activity_days": list(activity.keys())[::-1],
            "activity_values": list(activity.values())[::-1],

            # Топ категория
            "top_category": top_category,
            "top_category_proportion": top_category_proportion,

            "form": UserUpdateForm(instance=self.request.user),
        }
        return context