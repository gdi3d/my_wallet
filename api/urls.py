from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.views import ItemViewSet, TransactionViewSet, CategoryViewSet, WalletViewSet, WalletTotalViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', ItemViewSet, base_name='item')
router.register(r'transactions', TransactionViewSet, base_name='wallet')
router.register(r'category', CategoryViewSet, base_name='category')
router.register(r'wallet', WalletViewSet, base_name='wallet')
router.register(r'wallet-total', WalletTotalViewSet, base_name='wallet-total')
#router.register(r'full', WalletHistoryViewSet.as_view(), base_name='full')


urlpatterns = patterns("",
                        url(r'v1/', include(router.urls))
)
"""

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wallet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),  
    
)
"""