from datetime import datetime, date


def date_to_string(date, format):
    return date.strftime(format)

def string_to_date(str, format):
    return datetime.strptime(str, format)

def month_delta(date, delta):
    month = (date.month + delta) % 12
    year = date.year + ((date.month) + delta - 1) // 12
    if not month: month = 12
    day = min(date.day, 
    	[31,29 if year % 4 == 0 and not year % 400 == 0 else 28,31,30,31,30,31,31,30,31,30,31][month - 1])

    return date.replace(day=day, month=month, year=year)