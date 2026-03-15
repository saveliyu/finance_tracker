from django.db.models import Sum

from django.utils import timezone



def get_profile_stats(purchase):
    user_sum = purchase.aggregate(Sum('price'))['price__sum'] or 0
    user_month = purchase.filter(date__month=timezone.now().month)
    user_month_sum = user_month.aggregate(Sum('price'))['price__sum'] or 0
    user_month_cats = user_month.values('category').distinct().count()

    return {'user_sum': user_sum, 'user_month_sum': user_month_sum, 'user_month_cats': user_month_cats}