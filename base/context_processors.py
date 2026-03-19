from django.utils import timezone

def user_text_color(request):
    if not request.user.is_authenticated:
        return {}
    hex_color = str(request.user.color).strip('#')
    print(hex_color)
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # яркость (luminance)
    brightness = (r * 299 + g * 587 + b * 114) / 1000

    context = {}

    if brightness > 150:
        context['user_text_color'] = 'black'
    else:
        context['user_text_color'] = 'white'

    return context

def table_url(request):
    month = timezone.now().strftime("%B").lower()
    year = timezone.now().year

    context = {
        'url_month': month,
        'url_year': year
    }
    print('table', context)
    return context