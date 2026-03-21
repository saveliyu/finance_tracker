from datetime import timedelta
from pprint import pprint

from django.db.models import Sum

from django.utils import timezone
from base.models import Category


def get_profile_stats(purchase):
    user_sum = purchase.aggregate(Sum('price'))['price__sum'] or 0
    user_month = purchase.filter(date__month=timezone.now().month)
    user_month_sum = user_month.aggregate(Sum('price'))['price__sum'] or 0
    user_month_cats = user_month.values('category').distinct().count()

    return {'user_sum': user_sum, 'user_month_sum': user_month_sum, 'user_month_cats': user_month_cats}


def get_streak(purchases):
    purchases = purchases.values('date').distinct().order_by('-date')
    streak = 0
    prev_date = None
    for purchase in purchases:
        if streak == 0:
            streak = 1
        else:
            if purchase['date'] != prev_date:
                if (prev_date - purchase['date']) == timedelta(days=1):
                    streak += 1
                else:
                    break
        prev_date = purchase['date']
    return streak


def _get_day_moth(date):
    if len(str(date.day)) == 1:
        day = f'0{date.day}'
    else:
        day = f'{date.day}'
    if len(str(date.month)) == 1:
        month = f'0{date.month}'
    else:
        month = f'{date.month}'
    return f'{day}.{month}'


def get_activity_days(purchases):
    today = timezone.now().date()
    end_date = today - timedelta(days=30)
    purchases = purchases.filter(date__lte=today, date__gte=end_date).order_by('-date')
    activity = dict()
    for i in range(30):
        activity[_get_day_moth(today - timedelta(days=i))] = 0

    for purchase in purchases:
        date = _get_day_moth(purchase.date)
        price = float(purchase.price)
        activity[date] = price

    return activity


def get_top_category(purchases):
    purchases = purchases.filter(date__month=timezone.now().month)
    categories = purchases.values('category').distinct().order_by('category')

    best_category = None
    max_counts = 0
    for category in categories:
        counts = purchases.filter(category__pk=category['category']).count()

        if max_counts < counts:
            max_counts = counts
            best_category = category['category']
    category = Category.objects.get(pk=best_category)
    total_count = purchases.count()
    if max_counts > 0:
        proportion = round(total_count / max_counts)
    else:
        proportion = 0
    return category, proportion
