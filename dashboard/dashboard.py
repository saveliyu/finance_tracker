from django.db.models import Sum

from base.models import Category, Purchase


def get_parrent_category_dashboard_data(purchases, categories) -> dict:
    category_data = purchases.values('category__parent__id', 'category__parent__name').annotate(total=Sum('price'))
    category_labels = []
    category_totals = []
    category_colors = []

    for c in category_data:
        category_labels.append(c['category__parent__name'])
        category_totals.append(float(c['total']))
        category_obj = categories.get(id=c['category__parent__id'])
        category_colors.append(category_obj.color)
    return {'category_labels': category_labels,
        'category_totals': category_totals,
        'category_colors': category_colors,}

def get_category_dashboard_data(purchases, categories) -> dict:
    category_data = purchases.values('category__id', 'category__name').annotate(total=Sum('price'))
    category_labels = []
    category_totals = []
    category_colors = []

    for c in category_data:
        category_labels.append(c['category__name'])
        category_totals.append(float(c['total']))
        category_obj = categories.get(id=c['category__id'])
        category_colors.append(category_obj.color)
    return {'category_labels': category_labels,
        'category_totals': category_totals,
        'category_colors': category_colors,}

def get_person_dashboard_data(purchases, users) -> dict:
    person_data = purchases.values('user__id', 'user__username').annotate(total=Sum('price'))
    person_labels = []
    person_totals = []
    person_colors = []

    for p in person_data:
        person_labels.append(p['user__username'])
        person_totals.append(float(p['total']))
        user_obj = users.get(id=p['user__id'])
        person_colors.append(user_obj.color)

    return {'person_labels': person_labels,
        'person_totals': person_totals,
        'person_colors': person_colors,}

def get_products_per_day(purchases) -> dict:
    category = Category.objects.get(slug='eda')
    products_per_day = purchases.filter(category__parent=category).aggregate(Sum('price'))['price__sum'] or 0
    if products_per_day == 0:
        return {'products_per_day': 0}
    else:
        products_per_day /= (purchases[0].date.day - purchases.last().date.day)
        return {'products_per_day': products_per_day}


def get_data_for_dashboard(clean_purchases, purchases, categories, users, parents=None) -> dict:
    if parents:
        category_data = get_parrent_category_dashboard_data(clean_purchases, categories)
    else:
        category_data = get_category_dashboard_data(clean_purchases, categories)
    person_data = get_person_dashboard_data(purchases, users)

    products_per_day = get_products_per_day(clean_purchases)

    return {
        **category_data,
        **person_data,
        **products_per_day}