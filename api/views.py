from django.shortcuts import render
from django.db import transaction
from django.core import serializers
from django.db.models import Sum

from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from api.serializers import ItemSerializer, TransactionSerializer, CategorySerializer, WalletSerializer, FavoriteItemSerializer, WalletTotalSerializer

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

    	transactions = Transaction.objects.filter(wallet__user=user)

    	if wallet:
    		transactions = transactions.filter(wallet = wallet)

    	return transactions    

    @transaction.atomic
    def create(self, request):
        data = request.data
        
        item = data['item']                
        item = ItemSerializer(data=item)
        
        # test validation to show all errors at once
        transaction = data['transaction']
        # fake id for validating
        transaction.update({'item_id': 0}) 
        transaction = TransactionSerializer(data=transaction)        

        item_error = item.is_valid()
        transaction_error = transaction.is_valid()
        
        if not item_error or not transaction_error:

            return Response(dict(item.errors.items() + transaction.errors.items()), status=status.HTTP_400_BAD_REQUEST)

        if item.is_valid():            
            item.save()
        else:
            return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)

        if item:            
            # set new item id
            transaction = data['transaction']
            if not transaction['date']:
                import time
                transaction.update({'date': time.strftime("%d/%m/%Y")})

            transaction.update({'item_id': item.data['id']})
            transaction = TransactionSerializer(data=transaction)            

            if transaction.is_valid():
                transaction.save()
            else:
                return Response(transaction.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(transaction.data, status=status.HTTP_201_CREATED)



    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

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

        
