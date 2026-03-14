from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from base.models import *
from .forms import InviteForm

from datetime import datetime

from family.models import FamilyInvite, FamilyMember


# Create your views here.
def family_view(request):
    family_members = list()
    if request.user.family_members:
        family_members = request.user.family_members.all()
    members = dict()
    for member in family_members:
        user_sum = Purchase.objects.filter(user=member.user).aggregate(Sum('price'))['price__sum']
        user_month = Purchase.objects.filter(user=member.user, date__month=datetime.now().month)
        user_month_sum = user_month.aggregate(Sum('price'))['price__sum']
        user_month_cats = user_month.values('category').distinct().count()
        members[member] = {'user_sum': user_sum, 'user_month_sum': user_month_sum, 'user_month_cats': user_month_cats}

    profile_data = members[request.user.family_members.get(user=request.user)]

    context = {
        'members': members,
        'profile_data': profile_data,
    }
    return render(request, 'family/family.html', context)

def create_invite(request):
    if request.user.family_object and not request.user.invites.exists():
        invite = FamilyInvite()
        invite.created_by = request.user
        invite.family = request.user.family_object
        invite.save()
    return redirect('family:user_invite')


def user_invite_view(request):
    if FamilyInvite.objects.filter(created_by=request.user).exists():
        invite = get_object_or_404(FamilyInvite, created_by=request.user)
    else:
        invite = None
    context = {
        'invite': invite,
    }
    return render(request, 'family/invite.html', context)

def enter_invite_view(request):
    form = InviteForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if FamilyInvite.objects.filter(code=code).exists():
                invite = FamilyInvite.objects.get(code=code)
                FamilyMember.objects.create(family=invite.family, user=request.user, status=0)
                invite.delete()
    return render(request, 'family/enter_invite.html', context)