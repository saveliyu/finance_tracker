from django.db.models import Sum
from django.shortcuts import render, redirect
from base.models import *
from .forms import InviteForm
from django.contrib import messages

from django.utils import timezone

from family.models import FamilyInvite, FamilyMember


def profile_family_view(request):
    family_members = request.user.family_members.all().order_by('-status')

    members = dict()

    for member in family_members:
        purchase = Purchase.objects.filter(user=member.user)
        user_sum = purchase.aggregate(Sum('price'))['price__sum']
        user_month = purchase.filter(date__month=timezone.now().month)
        user_month_sum = user_month.aggregate(Sum('price'))['price__sum']
        user_month_cats = user_month.values('category').distinct().count()
        members[member] = {'user_sum': user_sum, 'user_month_sum': user_month_sum, 'user_month_cats': user_month_cats}


    profile_member = family_members.filter(user=request.user).first()
    profile_data = members.get(profile_member)

    roots = bool(profile_member.status)

    context = {
        'members': members,
        'profile_data': profile_data,
        'roots': roots,
    }

    return render(request, 'family/family.html', context)


def create_invite(request):
    family = request.user.family_object

    if family and not request.user.invites.exists():
        invite = FamilyInvite(created_by=request.user, family=family)
        invite.save()

    return redirect('family:invite')


def delete_invite(request):
    request.user.invites.all().delete()

    return redirect('family:profile_family')


def login_by_invite(request, code):
    invite = FamilyInvite.objects.filter(code=code).first()

    if not invite:
        messages.error(request, 'Неверный код')
        return redirect('family:enter_invite')
    if FamilyMember.objects.filter(family=invite.family, user=request.user).exists():
        messages.error(request, 'Вы уже состоите в этой семье')
        return redirect('family:enter_invite')
    else:
        FamilyMember.objects.create(family=invite.family, user=request.user, status=0)
    invite.delete()

    return redirect('family:profile_family')


def invite_view(request):
    invite = FamilyInvite.objects.filter(created_by=request.user).first()

    return render(request, 'family/invite.html', {'invite': invite})


def enter_invite_view(request):
    form = InviteForm()

    if request.method == 'POST':
        form = InviteForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data['code']
            return redirect('family:login_by_invite', code=code)
    context = {
        'form': form,
    }


    return render(request, 'family/enter_invite.html', context)
