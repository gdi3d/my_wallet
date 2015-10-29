from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wallet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^', include('website.urls', namespace='website')),
    url(r'^', include('django.contrib.auth.urls')),
)
