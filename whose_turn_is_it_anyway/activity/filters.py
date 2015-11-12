from delorean import Delorean


def date_time_format(date_time, format='%Y-%m-%d %H:%M'):
    return date_time.strftime(format)


def date_time_to_local(date_time, timezone):
    # Assume naive datetime objects to be UTC
    assert date_time.tzinfo is None
    d = Delorean(date_time, timezone='UTC')
    d.shift(timezone)
    return d.datetime
