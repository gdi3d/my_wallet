from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('website.views',
    url(r'^dashboard', 'dashboard', name='dashboard'),
    url(r'^money/in/$|/out/$|/edit/$', 'money', name='money'),
    url(r'^history', 'history', name='history'),
    url(r'^wallet', 'wallet', name='wallet'),
    url(r'^category', 'category', name='category'),
)
