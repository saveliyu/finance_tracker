from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from base.forms import PurchaseForm, CategoryForm
from base.models import Category, Purchase

from datetime import datetime

from .arrows_url import *
from dashboard.dashboard import get_data_for_dashboard


class IndexView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        month = datetime.now().strftime("%B").lower()
        year = datetime.now().year

        context = {
            'month': month,
            'year': year
        }
        return context

@login_required(login_url='users:login')
def table_view(request, year=None, month=None):
    categories = Category.objects.all().order_by('-parent')
    users = get_user_model().objects.all()
    purchases = Purchase.objects.filter(date__year=year, date__month=list(MONTHS.keys()).index(month) + 1)
    clean_purchases = purchases
    if request.GET.get('user_filter'):
        user_filter = request.GET.get('user_filter')
        if user_filter != 'all':
            purchases = purchases.filter(user__username__icontains=user_filter)

    if request.GET.get('category_filter'):
        category_filter = request.GET.get('category_filter')
        if category_filter != 'all':
            category = Category.objects.get(slug=category_filter)
            if category.parent is None:
                purchases = purchases.filter(category__parent=category)
            else:
                purchases = purchases.filter(category=category)

    if request.GET.get('parents'):
        dashboard_data = get_data_for_dashboard(clean_purchases, purchases, categories, users, parents=True)
    else:
        dashboard_data = get_data_for_dashboard(clean_purchases, purchases, categories, users)

    if month not in MONTHS:
        return redirect('base:home')

    trans_month = MONTHS[month]
    arrows_url = get_arrows_url(year, month)

    form = PurchaseForm(initial={'user': request.user}, user=request.user)

    context = {
        'categories': categories,
        'users': users,
        'purchases': purchases,

        'month': trans_month,
        'year': year,
        'arrows_url': arrows_url,

        'form': form,

        **dashboard_data
    }

    return render(request, 'base/table.html', context)


@login_required(login_url='users:login')
def add_purchase_view(request):
    form = PurchaseForm(request.POST)
    if form.is_valid():
        if form.cleaned_data['user'] != request.user:
            return redirect(request.META.get('HTTP_REFERER', '/'))
        form.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='users:login')
def delete_purchase_view(request, pk):
    purchase = Purchase.objects.get(pk=pk)
    purchase.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='users:login')
def add_category_view(request):
    categories = Category.objects.all().order_by('parent')
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))

    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'base/category_form.html', context)
