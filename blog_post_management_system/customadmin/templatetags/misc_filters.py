import re
from datetime import timedelta

from django import template
from django.contrib.admin.utils import quote

register = template.Library()


@register.filter
def admin_urlname(value, arg):
    if value.model_name == "user":
        pattern = "%s:%s-%s" % ("user", "user", arg)
    elif value.model_name == "BlogPost":
        pattern = "%s:%s-%s" % ("blogpost", "blogpost", arg)
    # elif value.model_name == "activebreak":
    #     pattern = "%s:%s-%s" % ("activebreak", "activebreak", arg)
    # elif value.model_name == "activitylevel":
    #     pattern = "%s:%s-%s" % ("activitylevel", "activitylevel", arg)
    # elif value.model_name == "focus":
    #     pattern = "%s:%s-%s" % ("focus", "focus", arg)
    # elif value.model_name == "standuptimer":
    #     pattern = "%s:%s-%s" % ("timer", "timer", arg)
    # elif value.model_name == "bluetoothdevices":
    #     pattern = "%s:%s-%s" % ("devices", "device", arg)
    # elif value.model_name == "event":
    #     pattern = "%s:%s-%s" % ("events", "events", arg)
    # elif value.model_name == "campaign":
    #     pattern = "%s:%s-%s" % ("strategies", "campaign", arg)
    # elif value.model_name == "nudging":
    #     pattern = "%s:%s-%s" % ("strategies", "nudging", arg)
    # elif value.model_name == "faq":
    #     pattern = "%s:%s-%s" % ("strategies", "faq", arg)
    # elif value.model_name == "justplay":
    #     pattern = "%s:%s-%s" % ("just_play", "just-play", arg)
    # elif value.model_name == "challenge":
    #     pattern = "%s:%s-%s" % ("challenge", "challenge", arg)
    else:
        pattern = "%s:%s-%s" % ("customadmin", value.model_name, arg)
    return pattern


@register.filter
def admin_urlquote(value):
    return quote(value)


@register.inclusion_tag("customadmin/partials/list_boolean.html")
def show_check(value):
    return {"bool_val": value}


@register.filter
def filter_by_department(employees, name):
    return employees.filter(department=name).order_by("-created_at")


@register.filter
def substraction(value1: int, value2: int):
    return (value1 - value2) >= 1


@register.filter
def to_string(value):
    return str(value)


@register.filter
def find_degree(value):
    return int((360 * value) / 100)


@register.filter
def milliseconds_to_hh_mm_ss(second):
    # Create a timedelta object representing the duration in seconds
    duration = timedelta(seconds=second)
    # Extract hours, minutes, and seconds from the timedelta
    hours, remainder = divmod(duration.seconds + duration.days * 3600 * 24, 3600)
    minutes, seconds = divmod(remainder, 60)
    # Format the result as HH:MM:SS
    formatted_time = f"{hours}:{minutes:02d}:{seconds:02d}"

    return formatted_time


@register.filter
def div(numerator, denominator):
    """Divide the `numerator` with the `denominator`"""
    return numerator / denominator


@register.inclusion_tag("partials/breadcrumb.html")
def breadcrumb_trail(request):
    """
    Usage: {% breadcrumb_trail request %}
    """
    uuid_pattern = r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"

    crumbs = []

    # Replace health-manager with user as we need to redirect the user to the user list.
    path = request.path_info.replace("health-manager", "user").strip("/").split("/")
    url = ""

    # Remove UUID from array
    path_array = [item for item in path if not re.match(uuid_pattern, item)]

    for crumb in path_array:
        url += "/" + crumb
        crumbs.append({"url": url, "name": crumb.capitalize()})
    return {"breadcrumbs": crumbs}


@register.filter
def get_extension(filepath):
    return filepath.split(".")[-1]


@register.filter
def get_unit(value, unit):
    if unit == "CL":
        return f"{value} Kcal"
    elif unit == "DT":
        return f"{convert_kk_mm_format(value)}"
    elif unit == "WK":
        return f"{value} steps"
    elif unit == "ST":
        return f"{milliseconds_to_hh_mm_ss(value)} time"
    return value


@register.filter
def get_type(value):
    todo_dict = {
        "CL": "Calorie",
        "DT": "Distance",
        "WK": "Walking",
        "ST": "Standing",
    }
    return todo_dict.get(value, value)


@register.filter
def round_value(value: int, limit: int):
    return round(value, limit)


@register.filter
def convert_kk_mm_format(distance_in_km: float):
    km_2_meters = int(distance_in_km)
    kilometers = int(km_2_meters / 1000)
    meters = km_2_meters - (kilometers * 1000)
    return f"{kilometers} km {meters} m"


@register.filter
def get_name(value):
    return value.replace("files/", "")
