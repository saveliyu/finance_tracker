
MONTHS = {
    "january": "январь",
    "february": "февраль",
    "march": "март",
    "april": "апрель",
    "may": "май",
    "june": "июнь",
    "july": "июль",
    "august": "август",
    "september": "сентябрь",
    "october": "октябрь",
    "november": "ноябрь",
    "december": "декабрь",
}

def get_arrows_url(year, month):
    next_year, next_month = get_next_url(year, month)
    previous_year, previous_month = get_previous_url(year, month)
    return {'next_year': next_year, 'previous_year': previous_year, 'next_month': next_month, 'previous_month': previous_month}


def get_next_url(year, month):
    next_year = year
    next_month_index = list(MONTHS.keys()).index(month) + 1
    if next_month_index == 12:
        next_year += 1
        next_month_index = 0
    next_month = list(MONTHS.keys())[next_month_index]
    return str(next_year), str(next_month)


def get_previous_url(year, month):
    previous_year = year
    previous_month_index = list(MONTHS.keys()).index(month) - 1
    if previous_month_index == -1:
        previous_year -= 1
        previous_month_index = 11
    previous_month = list(MONTHS.keys())[previous_month_index]
    return str(previous_year), str(previous_month)