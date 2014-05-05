#coding: utf-8

from django import template
from django.template.defaultfilters import stringfilter

from app.libs.arrays import get_category
from app.libs.utils import make_api_key

register = template.Library()

@register.filter
def choise(array, key): 
	vals = filter(lambda x : x[0] == key, array)
	if vals:
		return vals[0][1]

@register.filter
def keyvalue(dict, key):
    return dict[key]

@register.filter
def cat2str(cat_id):
	return get_category(cat_id)

@register.filter
def calc_api_key(seed):
	return make_api_key(seed)

@register.filter
def cat(value1, value2):
	return str(value1) + str(value2)

@register.filter
def eq(value1, value2):
	return str(value1) == str(value2) 


@register.filter
@stringfilter
def truncate(value, arg):
	if not value:
		return ""
	size = int(arg)
	if len(value) > size:
		return value[:size] + u"…"
	return value