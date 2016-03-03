from django.shortcuts import render
from django.db import transaction
from django.core import serializers
from django.db.models import Sum, Q
import django_filters

from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from wallet.serializers import ItemSerializer, TransactionSerializer, CategorySerializer, WalletSerializer, WalletTotalSerializer, TransactionsTotalSerializer, TagSerializer, GraphSeriesSerializer

from wallet.models import Item, Transaction, Category, Wallet, Tag
from wallet.helpers import prev_month_range, prev_year_range

from rest_framework.permissions import IsAuthenticatedOrReadOnly

import operator
import calendar
import datetime
import time

# Create your views here.

def transaction_search(request):

    user = request.user
    wallet = request.GET.get('wallet')
    string = request.GET.get('string')
    category_id = request.GET.get('category_id')
    income = request.GET.get('income')
    outcome = request.GET.get('outcome')
    date = request.GET.get('date')

    transactions = Transaction.objects.filter(wallet__user=user)

    if wallet:
        transactions = transactions.filter(wallet = wallet)

    if string:
        # search multiple terms
        if ',' in string:
            string = [s.strip() for s in string.split(',')]
            
            notes = reduce(operator.or_, (Q(item__note__icontains = s) for s in string))
            category = reduce(operator.or_, (Q(item__category__name__icontains = s) for s in string))
            tags = reduce(operator.or_, (Q(item__tags__name__icontains = s) for s in string))

            transactions = transactions.filter(notes | category | tags)

        else:
        
            transactions = transactions.filter(Q(item__note__icontains = string) | Q(item__category__name__icontains = string) | Q(item__tags__name__icontains = string))

    if category_id:
        category_id = category_id.split(',')
        transactions = transactions.filter(item__category__id__in = category_id)

    if income and not outcome:
        transactions = transactions.filter(item__amount__gt = 0)
    
    if outcome and not income:
        transactions = transactions.filter(item__amount__lt = 0)

    if date:
        if 'range' in date:
            date = date.split('.')
            date[0] = date[0].replace('range', '')
            transactions = transactions.filter(date__range = date)
        
        elif date == 'prev_year':
        
            prev_year = prev_year_range()
            transactions = transactions.filter(date__range = [prev_year['start'], prev_year['end']])
        
        elif date == 'prev_month':
        
            prev_month = prev_month_range()
            transactions = transactions.filter(date__range = [prev_month['start'], prev_month['end']])
        
        elif date == 'current_year':
        
            today = datetime.datetime.today()
            last_date = datetime.date(today.year, 12, 31)
            first_date = datetime.date(today.year, 1, 1)            
            transactions = transactions.filter(date__range = [first_date, last_date])        
        
        elif date == 'current_month':
        
            today = datetime.datetime.today()
            last_date = calendar.monthrange(today.year, today.month)[1]
            last_date = datetime.date(today.year, today.month, last_date)
            first_date = datetime.date(today.year, today.month, 1)

            transactions = transactions.filter(date__range = [first_date, last_date])

    return transactions

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

    * **api/v1/transactions/?string=STRING**  
    Search items on transactions that has STRING on note, category or tag property

    * **api/v1/transactions/?category_id=CATEGORY_ID**  
    Search items on transactions that belongs to the specified CATEGORY_ID. If you want to choose multiple categories
    set the ids separated by a comma like category_id=1,2,3
    
    * **api/v1/transactions/?date=range2015-08-07.2015-10-23**
    Search date by range  
    
    * **api/v1/transactions/?date=prev_year**
    Search all transactions from the previous year
    
    * **api/v1/transactions/?date=prev_month**
    Search all transactions from the previous month

    * **api/v1/transactions/?date=current_year**
    Search all transactions from the current year

    * **api/v1/transactions/?date=current_month**
    Search all transactions from the current month

    """
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)  

    def get_queryset(self):
    	
        transactions = transaction_search(self.request)
    	return transactions.order_by('-date')

class TransactionTotalViewSet(generics.RetrieveAPIView):
    """
    Returns the total amount for transactions search

    Filters:

    * **api/v1/transactions-total/?wallet=WALLET_ID**

    * **api/v1/transactions-total/?string=STRING**  
    Search items on transactions that has STRING on note, category or tag property

    * **api/v1/transactions-total/?category_id=CATEGORY_ID**  
    Search items on transactions that belongs to the specified CATEGORY_ID. If you want to choose multiple categories
    set the ids separated by a comma like category_id=1,2,3

    * **api/v1/transactions/?date=range2015-08-07.2015-10-23**
    Search date by range  
    
    * **api/v1/transactions/?date=prev_year**
    Search all transactions from the previous year
    
    * **api/v1/transactions/?date=prev_month**
    Search all transactions from the previous month

    * **api/v1/transactions/?date=current_year**
    Search all transactions from the current year

    * **api/v1/transactions/?date=current_month**
    Search all transactions from the current month
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):

        transactions = transaction_search(self.request)
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

class GraphicsViewSet(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, wallet_id):

        transactions = transaction_search(self.request).filter(wallet = wallet_id)

        aggregated = dict()

        # group amounts by year_month
        # on a dict
        for t in transactions:
            # convert date to timestamp to make it
            # easy to sort in the next for
            date = datetime.date(t.date.year, t.date.month, 1)
            date = time.mktime(date.timetuple())

            year_month = '%s' % date
            if year_month not in aggregated:
                aggregated[year_month] = 0

            aggregated[year_month] += t.item.amount

        data = list()
        first = False

        # iterate the aggregated dict sorting the key
        # to make the graphic ordered by date
        for k, v in sorted(aggregated.iteritems()):
            # convert to a standard yyyy-mm-dd
            year_month = datetime.date.fromtimestamp(float(k))

            # if it's the first iteration add
            # the initial wallet amount
            if not first:
                # get wallet initial ammount
                w = Wallet.objects.get(pk=wallet_id)
                aggregated = v + w.initial_amount
                first = True
            else:
                aggregated += v

            data.append({'year_month': year_month, 'amount': aggregated})
        
        serializer = GraphSeriesSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

