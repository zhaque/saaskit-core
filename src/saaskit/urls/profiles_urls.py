from django.conf.urls.defaults import *
from profiles import views
from saaskit.forms import UserProfileForm
from saaskit.views import create_profile

urlpatterns = patterns('',
    url(r'^create/$', create_profile, {
        'success_url': 'profiles_edit_profile',
        'form_class': UserProfileForm,
    }, name='profiles_create_profile'),

    url(r'^edit/$', views.edit_profile, {
        'success_url': 'profiles_edit_profile',
        'form_class': UserProfileForm,
    }, name='profiles_edit_profile'),

    url(r'^(?P<username>\w+)/$', views.profile_detail, {
        'public_profile_field': 'is_public'
    }, name='profiles_profile_detail'),

    url(r'^$', views.profile_list, {
        'public_profile_field': 'is_public'
    }, name='profiles_profile_list'),
)
