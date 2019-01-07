"""
Contains utilities used by more than one blueprint.
Otherwise, utilities are found in a dedicated utils file within
that blueprint.
"""

import pytz
from flask import abort
from datetime import datetime, timezone
from utils import parse_date
import http.client as httplib

utc = pytz.UTC


def safe_get_query_arg(request, arg_name):
    arg = request.args.get(arg_name)
    if not arg:
        abort(httplib.NOT_FOUND)
    return arg


def get_network_title(network):
    """Returns the title of a network given a network
    JSON as a dict
    """

    cur_country = network['country_cur']
    cur_region = network['region_cur']
    cur_city = network['city_cur']

    orig_country = network['country_origin']
    orig_region = network['region_origin']
    orig_city = network['city_origin']

    cur_location = ', '.join(
        [l for l in [cur_city, cur_region, cur_country] if l]
    )

    orig_location = ', '.join(
        [l for l in [orig_city, orig_region, orig_country] if l]
    )

    if network['network_class'] == '_l':

        # Language network
        language = network['language_origin']
        return "%s speakers in %s" % (language, cur_location)

    elif network['network_class'] == 'cc' \
            or network['network_class'] == 'rc' \
            or network['network_class'] == 'co':

        # City network (cc), region network (rc), or
        # country network (co).
        # Title-wise, we treat them all the same.

        return 'From %s in %s' % (orig_location, cur_location)

    else:
        return "Unknown"


def get_time_ago(past_time):
    """Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc

    Thanks: Stack Overflow id 1551382
    """

    now = datetime.now(timezone.utc)
    if type(past_time) is int:
        diff = now - datetime.fromtimestamp(past_time)
    elif isinstance(past_time, datetime):
        diff = now - past_time
    elif not past_time:
        diff = now - now
    elif isinstance(past_time, str):
        past_time = parse_date(past_time)
        diff = now - past_time
    else:
        return "unknown time ago"

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            if int(second_diff) == 1:
                return str(second_diff) + " second ago"
            else:
                return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            minutes = round(second_diff / 60)
            if int(minutes) == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            hours = round(second_diff / 3600)
            if int(hours) == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        if int(day_diff) == 1:
            return str(day_diff) + " day ago"
        else:
            return str(day_diff) + " days ago"
    if day_diff < 31:
        weeks = round(day_diff / 7)
        if int(weeks) == 1:
            return str(weeks) + " week ago"
        else:
            return str(weeks) + " weeks ago"

    if day_diff < 365:
        months = round(day_diff / 30)
        if int(months) == 1:
            return str(round(day_diff / 30)) + " month ago"
        else:
            return str(round(day_diff / 30)) + " months ago"

    years = round(day_diff / 365)
    if int(years) == 1:
        return str(years) + " year ago"
    else:
        return str(years) + " years ago"
