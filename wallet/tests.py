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
        

    def test_create_invalid_item(self):
        """ Create an invalid item """
        data = {'category_id':2, 'amount': None, 'note':"Hey! i'm testing this api"}
        r = self.client.post('/api/v1/items/', data)

        # check status code
        self.assertEqual(r.status_code, 400)        

    def test_create_item_no_category(self):
        """ Create a item with no category """
        data = {'category_id': '', 'amount': 9.5432, 'note':"Hey! i'm testing this api"}

        r = self.client.post('/api/v1/items/', data)
        
        # check if the item was created
        self.assertEqual(r.status_code, 201)

        data_returned = {'category': None, 'amount': "9.5432", 'note':"Hey! i'm testing this api", 'id': 2}
        
        self.assertEqual(r.data, data_returned)

    def test_update_item(self):
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

    def test_update_invalid_item(self):
        """
        Update an item with invalid data.
        """

        # invalids: item.amount (not exists)
        data = {
            "item": {'category_id': self.category.id, 'note':"Hey! i'm updating this api", 'id': self.item.id},
            "date": "2015/01/01",
            "wallet_id": 1,
            "id": 1
        }
        
        r = self.client.put('/api/v1/transactions/'+str(data['id'])+'/', json.dumps(data), follow=True, content_type="application/json")

        # validate the response code
        self.assertEqual(r.status_code, 400)

        # validate returned invalid fields        
        self.assertTrue(r.data['item'].has_key('amount'))

class CategoryTestCase(TestCase):

    def setUp(self):
        # Create an admin
        self.user = User.objects.create_user('test', 'test@domain.com', 'test')
        self.user.is_superuser = True
        self.user.save()

        # Every test needs a client.
        self.client = APIClient()
        self.request = APIRequestFactory()
        r = self.client.post('/api/v1/auth/login/', {'username':'test','password':'test'})

        self.base_url = '/api/v1/category/'

    def test_create_category(self):
        """ Create a category """

        category = {'name': 'category #1234'}

        r = self.client.post(self.base_url, category)

        # validate if created
        self.assertEqual(r.status_code, 201)

        # validate returned data
        category['id'] = 1
        self.assertEqual(r.data, category)

    def test_create_invalid_category(self):
        """ Try to create a category without name """

        r = self.client.post(self.base_url, {})

        # validate if created
        self.assertEqual(r.status_code, 400)

        # validate returned invalid field
        self.assertTrue(r.data.has_key('name'))

    def test_update_category(self):

        category = Category.objects.create(name='test category', user=self.user)

        data = {'name': 'Update Category', 'id': category.id}

        r = self.client.put(self.base_url + str(category.id) + '/', json.dumps(data), follow=True, content_type='application/json')

        # validate response code
        self.assertEqual(r.status_code, 200)

        # validate returned data
        self.assertJSONEqual(json.dumps(r.data), json.dumps(data))


class TransactionTestCase(TestCase):

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

        self.base_url = '/api/v1/transactions/'

    def test_create_transaction(self):
        """ Create a transaction """

        data = {
            "item": {'category_id': self.category.id, 'amount': "9.5432", 'note':"Hey! i'm creating a transaction"},
            "date": "2015/01/01",
            "wallet_id": self.wallet.id            
        }
        
        r = self.client.post(self.base_url, json.dumps(data), follow=True, content_type="application/json")

        # validate the response code
        self.assertEqual(r.status_code, 201)

        # validate returned data
        expected_result = {
            "item": {
                'category': {'name': str(self.category.name), 'id': self.category.id}, 
                'amount': "9.5432", 
                'note': "Hey! i'm creating a transaction",
                'id': 2,
            },
            "date": str(self.transaction.date.date()),
            "wallet": {
                'id': self.wallet.id,
                'name': self.wallet.name,
                'initial_amount': str(self.wallet.initial_amount), 
                'note': self.wallet.note
            },
            'id': 2
        }

        self.assertJSONEqual(json.dumps(r.data), json.dumps(expected_result))

    def test_create_invalid_transaction(self):
        """
        Try to create an invalid transaction
        """

        data = {
            "item": {'category_id': self.category.id, 'note':"Hey! i'm creating a transaction"},
            "wallet_id": self.wallet.id            
        }
        
        r = self.client.post(self.base_url, json.dumps(data), follow=True, content_type="application/json")

        # validate the response code
        self.assertEqual(r.status_code, 400)      

        # validate returned invalid fields        
        self.assertTrue(r.data.has_key('date'))
        self.assertTrue(r.data['item'].has_key('amount'))

    def test_update_transaction(self):
        """
        Update a transaction
        """

        data = {
            "item": {'category_id': self.category.id, 'amount': "1.12", 'note':"Hey! i'm updating a transaction"},
            "date": "2015/01/01",
            "wallet_id": self.wallet.id,
            'id': self.transaction.id
        }
        
        r = self.client.put(self.base_url + str(self.transaction.id) + '/', json.dumps(data), follow=True, content_type="application/json")

        # validate the response code
        self.assertEqual(r.status_code, 200)

        # validate returned data
        expected_result = {
            "item": {
                'category': {'name': str(self.category.name), 'id': self.category.id}, 
                'amount': "1.1200", 
                'note': "Hey! i'm updating a transaction",
                'id': 1,
            },
            "date": '2015-01-01',
            "wallet": {
                'id': self.wallet.id,
                'name': self.wallet.name,
                'initial_amount': str(self.wallet.initial_amount), 
                'note': self.wallet.note
            },
            'id': 1
        }

        self.assertJSONEqual(json.dumps(r.data), json.dumps(expected_result))

class WalletTestCase(TestCase):
    
    def setUp(self):
        # Create an admin
        self.user = User.objects.create_user('test', 'test@domain.com', 'test')
        self.user.is_superuser = True
        self.user.save()

        # Every test needs a client.
        self.client = APIClient()
        self.request = APIRequestFactory()
        r = self.client.post('/api/v1/auth/login/', {'username':'test','password':'test'})

        self.wallet = Wallet.objects.create(name='Test Wallet', initial_amount=50.3212, note='Me', user=self.user)

        self.base_url = '/api/v1/wallet/'

    def test_create_wallet(self):

        data = {'name': "i'm a new wallet", 'initial_amount': "500.1212", 'note': 'the new wallet'}

        r = self.client.post(self.base_url, data)

        # validate status response
        self.assertEqual(r.status_code, 201)

        # validate returned data
        data['id'] = 2
        self.assertEqual(r.data, data)

    def test_invalid_wallet(self):
        """
        Try to create a wallet without name
        """

        data = {'initial_amount': "500.1212", 'note': 'the new wallet'}

        r = self.client.post(self.base_url, data)

        # validate status response
        self.assertEqual(r.status_code, 400)

        # validate returned invalid fields
        self.assertTrue(r.data.has_key('name'))

    def test_update_wallet(self):

        data = {'name': 'Updated wallet', 'initial_amount': "500.1212", 'note': 'updating the wallet', 'id': self.wallet.id}

        r = self.client.put(self.base_url + str(self.wallet.id) + '/', json.dumps(data), follow=True, content_type='application/json')

        # validate response code
        self.assertEqual(r.status_code, 200)

        # validate returned data
        self.assertJSONEqual(json.dumps(r.data), json.dumps(data))