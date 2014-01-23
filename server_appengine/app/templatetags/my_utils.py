#coding: utf-8
from django import template

register = template.Library()

@register.filter
def value(dict, key): 
    return dict[key][1]