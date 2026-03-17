from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from base.models import *
from .forms import InviteForm
from django.contrib import messages

from family.models import FamilyInvite
from family.utils import *

from users.models import *


def profile_family_view(request):
    if request.method == 'POST':
        member_status = request.POST.get('member_status')
        member_pk = request.POST.get('member_pk')

        member = CustomUser.objects.get(pk=member_pk).family_member

        member.status = int(member_status)
        member.save()

        return redirect('family:profile_family')

    family_member = request.user.get_family_member

    if not family_member:
        return render(request, 'family/family.html', {
            'profile_data': get_profile_stats(Purchase.objects.filter(user=request.user)),
            'roots': False,
        })

    users = CustomUser.objects.filter(
        family_member__family=family_member.family
    )

    all_purchases = Purchase.objects.filter(user__in=users)
    members = dict()
    for user in users:
        members[user] = get_profile_stats(all_purchases.filter(user=user))

    profile_data = members.get(request.user)
    roots = bool(family_member.status)
    statuses = [x for x in FamilyMember.Status.choices if x[0] != FamilyMember.Status.CREATOR]

    context = {
        'members': members,
        'profile_data': profile_data,
        'roots': roots,
        'statuses': statuses,
    }

    return render(request, 'family/family.html', context)


def create_family_view(request):
    return render(request, 'family/create_family.html')


@login_required(login_url='users:login')
def invite_view(request):
    invites = FamilyInvite.objects.filter(created_by=request.user)
    if invites:
        invite = invites.first()
    else:
        return redirect('family:create_invite')

    return render(request, 'family/invite.html', {'invite': invite})


@login_required(login_url='users:login')
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


@login_required(login_url='users:login')
def create_invite(request):
    family = request.user.family_object

    if family and not hasattr(request.user, 'invites'):
        invite = FamilyInvite(created_by=request.user, family=family)
        invite.save()

    return redirect('family:invite')


@login_required(login_url='users:login')
def delete_invite(request):
    if hasattr(request.user, 'invites'):
        request.user.invites.delete()

    return redirect('family:create_invite')


def login_by_invite(request, code):
    invite = FamilyInvite.objects.filter(code=code).first()

    if not invite:
        messages.error(request, 'Неверный код')
        return redirect('family:enter_invite')
    if FamilyMember.objects.filter(family=invite.family, user=request.user).exists():
        messages.error(request, 'Вы уже состоите в этой семье')
        return redirect('family:enter_invite')
    if FamilyMember.objects.filter(user=request.user).exists():
        messages.error(request, 'Вы уже состоите в другой семье')
        return redirect('family:enter_invite')
    else:
        FamilyMember.objects.create(family=invite.family, user=request.user, status=0)
    invite.delete()

    return redirect('family:profile_family')


def delete_member(request, pk):
    family_member = FamilyMember.objects.filter(user__pk=pk).first()
    if family_member:
        member = family_member.user
    else:
        messages.success(request, f'Такого пользователя не существует')
        return redirect('family:profile_family')

    user = request.user
    if member == user:
        member.family_member.delete()
        messages.success(request, f'Вы успешно вышли из семьи')
    elif not member.family_object:
        messages.error(request, 'Данный пользователь на данный момент не состоит в семье')
    elif member.family_object != user.family_object:
        messages.error(request, 'Вы не можете удалить члена другой семьи')
    elif not user.family_member.status:
        messages.error(request, 'У вас не хватает прав для удаления')
    elif member.family_member.status == 1:
        messages.error(request, 'Вы не можете удалить создателя семьи')
    else:
        member.family_member.delete()
        messages.success(request, f'Пользователь {member} удален')

    return redirect('family:profile_family')
