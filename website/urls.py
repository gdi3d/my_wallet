from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('website.views',
    url(r'^$', 'home', name='home'),
    url(r'^dashboard', 'dashboard', name='dashboard'),
    url(r'^money/new/$', 'money', name='money_new'),
    url(r'^money/edit/(?P<pk>\d+)/$', 'money', name='money_edit'),
    url(r'^history', 'history', name='history'),
    url(r'^wallet', 'wallet', name='wallet'),
    url(r'^category', 'category', name='category'),
)
