from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('website.views',
    url(r'^$', 'home', name='home'),
    url(r'^dashboard', 'dashboard', name='dashboard'),
    url(r'^money/new/in/$', 'money', name='money_new_in'),
    url(r'^money/new/out/$', 'money', name='money_new_out'),
    url(r'^money/edit/(?P<pk>\d+)/$', 'money', name='money_edit'),
    url(r'^history', 'history', name='history'),
    url(r'^wallet', 'wallet', name='wallet'),
    url(r'^category', 'category', name='category'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
)
