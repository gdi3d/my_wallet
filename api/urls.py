from django.conf.urls import patterns, include, url

urlpatterns = patterns("",    
    url(r'^v1/auth/', include('rest_auth.urls')),
    url(r'^v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^v1/', include('wallet.urls')),
)