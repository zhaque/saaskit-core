# http://code.djangoproject.com/ticket/361
from django import template
register = template.Library()

def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)
mult.is_safe = False

def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)
sub.is_safe = False

def div(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg)
div.is_safe = False

register.filter('mult', mult)
register.filter('sub', sub)
register.filter('div', div)
