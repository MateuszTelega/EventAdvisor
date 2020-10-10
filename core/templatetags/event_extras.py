from django.template import Library
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import SafeString


register = Library()


@register.simple_tag
def event_title_format(event, short=True):
    if short:
        return f'{event.title}'
    return f'{event.title} ({event.date_from}) - {event.event_type}'


@register.simple_tag
def event_date_format(event):
    dt = event.date_from
    tm = event.start_time
    minutes = str(tm.minute)
    if tm.minute < 10:
        minutes = '0' + minutes
    if dt.year != timezone.now().year:
        return f'{dt.strftime("%B")} {dt.strftime("%d")}, {dt.strftime("%Y")}, {dt.strftime("%A")}' \
            f' - {tm.hour}:{minutes}'
    return f'{dt.strftime("%B")} {dt.strftime("%d")}, {dt.strftime("%A")} - {tm.hour}:{minutes}'


@register.simple_tag
def event_description_format(event):
    if len(event.description) > 50:
        return f'{event.description[:50]} (...)'
    return f'{event.description}'


@register.filter
def attr_as_p(obj, attrname):
    label = escape(attrname.capitalize())
    val = getattr(obj, attrname)
    if val:
        if attrname == 'start_time':
            minutes = str(val.minute)
            if val.minute < 10:
                minutes = '0' + minutes
            val = f'{val.hour}:{minutes}'
    else:
        val = ''

    value = escape(val)
    return SafeString(f'<p><strong>{label}:</strong> {value}</p>')
