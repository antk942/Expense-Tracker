from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def getDebugSetting():
    return settings.DEBUG