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


import pymongo
import lifestream.mongodb as mongodb

PAGE_SIZE = 50

def latest_activity(context, page=1):
    collection = mongodb.get_collection()
    object_list = collection.find().sort('lifestream:timestamp', pymongo.DESCENDING ).limit(PAGE_SIZE).skip((page-1)*PAGE_SIZE)
    to_return = {
        'object_list': list(object_list),
    }
    return to_return

register.inclusion_tag('lifestream/_activity_list.html', takes_context=True)(latest_activity)