from django import template
import jdatetime

register = template.Library()

@register.filter
def to_jalali(date):
    if date:
        return jdatetime.date.fromgregorian(date=date).strftime('%Y/%m/%d')
    return ''