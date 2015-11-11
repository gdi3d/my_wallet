import datetime

def prev_month_range(when = None):
    """Return (previous month's start date, previous month's end date)."""
    if not when:
        # Default to today.
        when = datetime.datetime.today()
    # Find previous month: http://stackoverflow.com/a/9725093/564514
    # Find today.
    first = datetime.date(day=1, month=when.month, year=when.year)
    # Use that to find the first day of this month.
    prev_month_end = first - datetime.timedelta(days=1)
    prev_month_start = datetime.date(day=1, month= prev_month_end.month, year= prev_month_end.year)
    # Return previous month's start and end dates in YY-MM-DD format.
    return {'start': prev_month_start, 'end':prev_month_end}

def prev_year_range(when = None):
    """Returns the previous year range from Jan 1 to Dec 31"""
    if not when:
        # Default to today.
        when = datetime.datetime.today()
        # Find today.
    prev_year = when.year - 1
    # Use that to find the first day of this month.
    first_day_year = datetime.date(day=1, month=1, year=prev_year)
    last_day_year = datetime.date(day=31, month=12, year=prev_year)
    # Return previous month's start and end dates in YY-MM-DD format.
    return {'start': first_day_year, 'end': last_day_year}


def last_30_days():
    return datetime.datetime.today() + datetime.timedelta(-30)