# _*_ coding:utf-8 _*_
__author__ = '111'
__date__ = '2018/1/8 22:23'
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def star_key_format(value):
    format_tel = value[0:3] + " " + "****" + " " + value[7:]
    return mark_safe(format_tel)

#自定义过滤器，在当前应用下