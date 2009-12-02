### -*- coding: utf-8 -*- ####################################################
from django.contrib.flatpages.models import FlatPage
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe

from django.contrib.flatpages.views import DEFAULT_TEMPLATE

from muaccount_content.models import MUFlatPage

def flatpage(request, url, queryset=FlatPage.objects.all()):
    """improved default view by extra parameter queryset instead hard-coded FlatPage"""
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_404(queryset, url__exact=url, sites__id__exact=settings.SITE_ID)
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    c = RequestContext(request, {
        'flatpage': f,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, FlatPage, f.id)
    return response


def mu_flatpage(request, url, queryset=MUFlatPage.objects.all()):
    if not url.startswith('/'):
        url = "/" + url
    try:
        customized = queryset.get(url__exact=url, 
                            sites__id__exact=settings.SITE_ID, 
                            muaccount=request.muaccount)

        if customized.active:
            if not customized.use_default:
                return flatpage(request, url, queryset.filter(muaccount=request.muaccount))
        else:
            raise Http404('Current page %s is not active.' % url)

    except queryset.model.DoesNotExist:
        pass
    
    return flatpage(request, url, queryset.filter(muaccount__exact=None, active__exact=True))    
