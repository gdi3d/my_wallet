from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core import serializers

from rest_framework.test import APIClient, APIRequestFactory

from wallet.models import *

import json
import datetime

# Create your tests here.
class ItemTestCase(TestCase):

    def setUp(self):
        
        # Create an admin
        u = User.objects.create_user('test', 'test@domain.com', 'test')
        u.is_superuser = True
        u.save()

        # Every test needs a client.
        self.client = APIClient()
        self.request = APIRequestFactory()
        r = self.client.post('/api/v1/auth/login/', {'username':'test','password':'test'})

        self.category = Category.objects.create(name='test category', user=u)
        self.item = Item.objects.create(category=self.category, amount=19.2256, note="Hello! i'm a nice item!")
        self.wallet = Wallet.objects.create(name='Test Wallet', initial_amount=50.3212, note='Me', user=u)
        self.transaction = Transaction.objects.create(item=self.item, wallet=self.wallet, date=datetime.datetime.now())
        

    def test_create_item(self):              
        """ Create a new valid item """
        data = {'category_id': self.category.id, 'amount': 9.5432, 'note':"Hey! i'm testing this api"}

        r = self.client.post('/api/v1/items/', data)
        
        # check if the item was created
        self.assertEqual(r.status_code, 201)

        # check the data returned data
        category = dict()        
        category['name'] = self.category.name
        category['id'] = self.category.id

        data_returned = {'category': category, 'amount': "9.5432", 'note':"Hey! i'm testing this api", 'id': 2}
        
        self.assertEqual(r.data, data_returned)
        

    def test_create_item_no_amount(self):
        """ Create an new invalid item """
        data = {'category_id':2, 'amount': None, 'note':"Hey! i'm testing this api"}
        r = self.client.post('/api/v1/items/', data)

        # check status code
        self.assertEqual(r.status_code, 400)        

    def _test_create_item_no_category(self):
        """ Create a item with no category """
        data = {'category_id': '', 'amount': 9.5432, 'note':"Hey! i'm testing this api"}

        r = self.client.post('/api/v1/items/', data)
        
        # check if the item was created
        self.assertEqual(r.status_code, 201)

        data_returned = {'category': None, 'amount': "9.5432", 'note':"Hey! i'm testing this api", 'id': 2}
        
        self.assertEqual(r.data, data_returned)

    def test_edit_item(self):
        """
        Update an item.
        It won't work unless you update the transaction where the item is.
        This is because the get_queryset on the item view will return using the filter:
        transaction transaction__wallet__user=user
        """

        data = {
            "item": {'category_id': self.category.id, 'amount': "9.5432", 'note':"Hey! i'm updating this api", 'id': self.item.id},
            "date": "2015/01/01",
            "wallet_id": 1,
            "id": 1
        }
        
        r = self.client.put('/api/v1/transactions/'+str(data['id'])+'/', json.dumps(data), follow=True, content_type="application/json")

        # validate the response code
        self.assertEqual(r.status_code, 200)

        # validate the data
        expected_result = {
            "item": {'category': {'id': self.category.id, 'name': self.category.name}, 
                    'amount': "9.5432",
                    'note':"Hey! i'm updating this api", 'id': self.item.id
                    },
            "date": "2015-01-01",
            "wallet": {'name': self.wallet.name, 'id': self.wallet.id, 'initial_amount': str(self.wallet.initial_amount), 'note':self.wallet.note},
            "id": 1
        }
        
        self.assertJSONEqual(json.dumps(r.data), json.dumps(expected_result))

    def test_edit_invalid_item(self):
        """
        Update an item.
        It won't work unless you update the transaction where the item is.
        This is because the get_queryset on the item view will return using the filter:
        transaction **transaction__wallet__user=user**
        """

        # invalids: item.amount (not exists), date (format)
        data = {
            "item": {'category_id': self.category.id, 'note':"Hey! i'm updating this api", 'id': self.item.id},
            "date": "2015-01-01",
            "wallet_id": 1,
            "id": 1
        }
        
        r = self.client.put('/api/v1/transactions/'+str(data['id'])+'/', json.dumps(data), follow=True, content_type="application/json")

        # validate the response code
        self.assertEqual(r.status_code, 400)

        # validate returned invalid fields        
        self.assertTrue(r.data.has_key('date'))
        self.assertTrue(r.data['item'].has_key('amount'))        