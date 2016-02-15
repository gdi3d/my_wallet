from django.conf.urls import patterns, include, url
from wallet.views import ItemViewSet, TransactionViewSet, TransactionTotalViewSet, CategoryViewSet, WalletViewSet, WalletTotalViewSet, TagsViewSet, GraphicsViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', ItemViewSet, base_name='item')
router.register(r'transactions', TransactionViewSet, base_name='wallet')
router.register(r'category', CategoryViewSet, base_name='category')
router.register(r'wallet', WalletViewSet, base_name='wallet')
router.register(r'wallet-total', WalletTotalViewSet, base_name='wallet-total')
router.register(r'tags', TagsViewSet, base_name='tags')

urlpatterns = patterns("",
	url(r'^transactions-total/', TransactionTotalViewSet.as_view(), name='transactions-total'),
	url(r'^graphic/(?P<wallet_id>\d+)', GraphicsViewSet.as_view(), name='graphic-series'),
    url(r'', include(router.urls))
)