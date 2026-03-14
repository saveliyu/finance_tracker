from django.db.models import Sum
from django.shortcuts import render
from base.models import *

from datetime import datetime

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