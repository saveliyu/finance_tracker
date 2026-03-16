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

        member = CustomUser.objects.get(pk=member_pk).family.first()

        member.status = int(member_status)
        member.save()

        return redirect('family:profile_family')

    family_member = request.user.family.first()

    if not family_member:
        return render(request, 'family/family.html', {
            'profile_data': get_profile_stats(Purchase.objects.filter(user=request.user)),
            'roots': False,
        })

    users = CustomUser.objects.filter(
        family__family=family_member.family
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


def delete_member(request, pk):
    member = FamilyMember.objects.filter(user__pk=pk).first().user
    user = request.user
    if not member.family_object:
        messages.error(request, 'Данный пользователь на данный момент не состоит в семье')
    elif member == user:
        messages.error(request, 'Вы не можете удалить самого себя')
    elif member.family_object != user.family_object:
        messages.error(request, 'Вы не можете удалить члена другой семьи')
    elif not user.family.first().status:
        messages.error(request, 'У вас не хватает прав для удаления')
    elif member.family.first().status == 1:
        messages.error(request, 'Вы не можете удалить создателя семьи')
    else:
        member.family.all().delete()
        messages.success(request, f'Пользователь {member} удален')

    return redirect('family:profile_family')
