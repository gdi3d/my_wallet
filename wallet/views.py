from django.shortcuts import render
from django.db import transaction
from django.core import serializers
from django.db.models import Sum
import django_filters

from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from wallet.serializers import ItemSerializer, TransactionSerializer, CategorySerializer, WalletSerializer, WalletTotalSerializer, TransactionsTotalSerializer, TagSerializer

from wallet.models import Item, Transaction, Category, Wallet, Tag

from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    """
    Viewing and editing items.

    No filters options.
    """
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):

        user = self.request.user
        return Item.objects.filter(transaction__wallet__user=user)

class TransactionViewSet(viewsets.ModelViewSet):
    """
    Viewing and editing transactions.

    Filters:

    * **api/v1/transactions/?wallet=WALLET_ID**

    * **api/v1/transactions/?note=STRING**  
    Search items on transactions that has STRING on note property

    * **api/v1/transactions/?category=STRING**  
    Search items on transactions that belong to a category that has STRING on name property

    * **api/v1/transactions/?category_id=CATEGORY_ID**  
    Search items on transactions that belongs to the specified CATEGORY_ID. If you want to choose multiple categories
    set the ids separated by a comma like category_id=1,2,3
    """
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)  

    def get_queryset(self):

    	user = self.request.user
    	wallet = self.request.QUERY_PARAMS.get('wallet')
        note = self.request.GET.get('note')
        category = self.request.GET.get('category')
        category_id = self.request.GET.get('category_id')

    	transactions = Transaction.objects.filter(wallet__user=user)

    	if wallet:
    		transactions = transactions.filter(wallet = wallet)

        if note:
            transactions = transactions.filter(item__note__icontains = note)

        if category:
            transactions = transactions.filter(item__category__name__icontains = category)

        if category_id:
            category_id = category_id.split(',')
            transactions = transactions.filter(item__category__id__in = category_id)

    	return transactions

class TransactionTotalViewSet(generics.RetrieveAPIView):
    """
    Returns the total amount for transactions search

    Filters:

    * **api/v1/transactions-total/?wallet=WALLET_ID**

    * **api/v1/transactions-total/?note=STRING**  
    Search items on transactions that has STRING on note property

    * **api/v1/transactions-total/?category=STRING**  
    Search items on transactions that belong to a category that has STRING on name property

    * **api/v1/transactions-total/?category_id=CATEGORY_ID**  
    Search items on transactions that belongs to the specified CATEGORY_ID. If you want to choose multiple categories
    set the ids separated by a comma like category_id=1,2,3
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):

        user = self.request.user
        wallet = self.request.QUERY_PARAMS.get('wallet')
        note = self.request.GET.get('note')
        category = self.request.GET.get('category')

        transactions = Transaction.objects.filter(wallet__user=user)

        if wallet:
            transactions = transactions.filter(wallet = wallet)

        if note:
            transactions = transactions.filter(item__note__icontains = note)

        if category:
            transactions = transactions.filter(item__category__name__icontains = category)

        transactions = transactions.aggregate(total=(Sum('item__amount')))

        serializer = TransactionsTotalSerializer(transactions)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
    	user = self.request.user
    	return Category.objects.filter(user=user).order_by('name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WalletViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
    	
    	user = self.request.user
    	return Wallet.objects.filter(user=user).order_by('name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class WalletTotalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns the balance of all wallets

    Filters:

    * **api/v1/wallet-total/?wallet_id=ID**  
    Returns the specified balance for the wallet or wallets. If you want to choose multiple wallets
    set the ids separated by a comma like wallet_id=1,2,3
    """
    serializer_class = WalletTotalSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):

        user = self.request.user
        wallets = Wallet.objects.filter(user=user)
        wallet_id = self.request.GET.get('wallet_id')
        
        _total = Transaction.objects.filter(wallet__user=user)

        if wallet_id:
            wallet_id = wallet_id.split(',')
            _total = _total.filter(wallet__in=wallet_id)

        _total = _total.values('wallet').annotate(total=Sum('item__amount'))

        total = []
        for t in _total:
            for w in wallets:                
                if t['wallet'] == w.id:
                    total.append({'wallet': w, 'total': t['total']})

        return total

class TagsViewSet(viewsets.ModelViewSet):

    serializer_class = TagSerializer
    permission_classes = permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):

        search = self.request.GET.get('q')

        user = self.request.user
        tag = Tag.objects.filter(user=user)
        
        if search:
            tag = tag.filter(name__icontains=search)

        return tag

