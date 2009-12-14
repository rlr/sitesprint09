from django import template
from django.template import Context
from templatetag_sugar.register import tag
from templatetag_sugar.parser import Constant, Variable, Optional, Name

register = template.Library()

@register.filter(name='ls_key')
def ls_key(value, arg):
    "Gets the value in the dictionary value with specified key arg"
    return value.get(arg, "")

@register.filter(name='ls_date')
def ls_date(value, arg):
    return value[arg].date


@tag(register, [Variable(), Optional([Constant("as"), Name()])])
def timestampdate(context, val, asvar=None):
    date = val['lifestream:timestamp'].date()
    if asvar:
        context[asvar] = date
        return ""
    else:
        return date

@register.simple_tag
def ls_activity(activity):
    t = template.loader.get_template('lifestream/_'+activity['lifestream:provider']+'.html')
    return t.render(Context({'object': activity}))

