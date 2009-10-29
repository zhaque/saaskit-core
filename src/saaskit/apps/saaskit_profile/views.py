from django.shortcuts import redirect
from django.db.models import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from profiles.views import default_success_url
from saaskit_profile.forms import UserProfileForm


def create_profile(request, form_class=UserProfileForm, success_url=default_success_url,
                   template_name='profiles/create_profile.html',
                   extra_context=None):
    try:
        profile_obj = request.user.get_profile()
        return redirect('profiles_edit_profile')
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            profile_obj = form.save(user=request.user)
            if callable(success_url):
                success_url = success_url(profile_obj)
            return redirect(success_url)

    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)
create_profile = login_required(create_profile)
