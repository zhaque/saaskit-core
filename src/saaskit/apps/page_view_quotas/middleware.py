### -*- coding: utf-8 -*- ##

#from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
#import notification

from django_counter.models import ViewCounter

class PageViewQuotasMiddleware(object):
    
    def process_request(self, request):
        if not request.path.startswith(settings.MEDIA_URL) \
        and ViewCounter.objects.get_for_object(request.muaccount).count >= request.muaccount.owner.quotas.page_views + settings.GRACE_PAGE_VIEW \
        and request.path != reverse('muaccount_suspended'):
            return redirect('muaccount_suspended')
        