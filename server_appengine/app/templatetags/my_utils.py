#coding: utf-8

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def choise(array, key): 
	vals = filter(lambda x : x[0] == key, array)
	if vals:
		return vals[0][1]


@register.filter
def eq(value1, value2):
	return str(value1) == str(value2) 


@register.filter
@stringfilter
def truncate( value, arg):
	size = int(arg)
	if len(value) > size:
		return value[:size] + u"…"
	return value