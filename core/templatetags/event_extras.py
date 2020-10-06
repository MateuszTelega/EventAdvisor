from django.template import Library
from django.utils.html import escape
from django.utils.safestring import SafeString


register = Library()


@register.simple_tag
def event_format(event, short=True):
    if short:
        return f'{event.title}'
    return f'{event.title} ({event.date_from}) - {event.event_type}'


@register.filter
def attr_as_p(obj, attrname):
    label = escape(attrname.capitalize())
    value = escape(getattr(obj, attrname))
    return SafeString(f'<p><strong>{label}:</strong> {value}</p>')
