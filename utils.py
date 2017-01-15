from datetime import datetime, date


def date_to_string(date, format):
    return date.strftime(format)

def string_to_date(str, format):
    return datetime.strptime(str, format)