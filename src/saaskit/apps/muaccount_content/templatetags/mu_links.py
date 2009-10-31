### -*- coding: utf-8 -*- ####################################################
#
# Copyright (c) 2009 Arvid Paeglit. All Rights Reserved.
#
##############################################################################
"""
$Id:interfaces.py 11316 2008-05-19 12:07:19Z arvid $
"""

from django import template

from django.db.models.aggregates import Count, Max
from django.db.models import F

from muaccount_content.models import MUFlatPage, mu_queryset

register = template.Library()  

class LinksNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = mu_queryset(context['request'].muaccount, 
                                             MUFlatPage.objects.all(), 'url')\
                                .filter(show_link__exact=True, active__exact=True)
        return ''

def do_get_links(parser, token):
    bits = token.contents.split()
    if len(bits) == 3:
        if bits[1] != 'as':
            raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
        return LinksNode(bits[2])
    else:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]

register.tag('get_links', do_get_links)
