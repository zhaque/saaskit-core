### -*- coding: utf-8 -*- ##

from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django_counter.models import ViewCounter
from quotas import Unlimited

class PageViewQuotasMiddleware(object):
    
    def process_request(self, request):
        if request.muaccount.owner:
            page_views = request.muaccount.owner.quotas.page_views
            if not request.path.startswith(settings.MEDIA_URL) \
            and not isinstance(page_views, Unlimited) \
            and ViewCounter.objects.get_for_object(request.muaccount).count >= page_views + settings.GRACE_PAGE_VIEW \
            and request.path != reverse('muaccount_suspended'):
                return redirect('muaccount_suspended')
        