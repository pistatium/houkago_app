#coding: utf-8
from django import template

register = template.Library()

@register.filter
def choise(array, key): 
	vals = filter(lambda x : x[0] == key, array)
	if vals:
		return vals[0][1]


@register.filter
def eq(value1, value2):
	return str(value1) == str(value2) 


