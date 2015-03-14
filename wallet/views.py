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

from wallet.serializers import ItemSerializer, TransactionSerializer, CategorySerializer, WalletSerializer, FavoriteItemSerializer, WalletTotalSerializer, TransactionsTotalSerializer

from wallet.models import Item, Transaction, Category, Wallet, FavoriteItem

from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):

        user = self.request.user
        return Item.objects.filter(transaction__wallet__user=user)

class FavoriteItemViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    serializer_class = FavoriteItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):

        user = self.request.user
        return FavoriteItem.objects.filter(user=user)

class TransactionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)  

    def get_queryset(self):

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

    	return transactions

class TransactionTotalViewSet(generics.RetrieveAPIView):

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

    serializer_class = WalletTotalSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):

        user = self.request.user
        wallets = Wallet.objects.filter(user=user)
        
        _total = Transaction.objects.filter(wallet__user=user).values('wallet').annotate(total=Sum('item__amount'))

        total = []
        for t in _total:
            for w in wallets:                
                if t['wallet'] == w.id:
                    total.append({'wallet': w, 'total': t['total']})

        return total

        
