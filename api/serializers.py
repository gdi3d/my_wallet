from django.contrib.auth.models import User, Group
from rest_framework import serializers
import datetime

from wallet.models import Wallet, Item, Transaction, Category, FavoriteItem

class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		exclude = ('user', )

class ItemSerializer(serializers.ModelSerializer):

	category = CategorySerializer(read_only=True)
	category_id = serializers.IntegerField(write_only=True)	

	class Meta:
		model = Item

class WalletSerializer(serializers.ModelSerializer):

	class Meta:
		model = Wallet
		exclude = ('user',)


class FavoriteItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = FavoriteItem

class TransactionSerializer(serializers.ModelSerializer):

	item = ItemSerializer(read_only=True)
	item_id = serializers.IntegerField(write_only=True)
	
	wallet = WalletSerializer(read_only=True)
	wallet_id = serializers.IntegerField(write_only=True)

	date = serializers.DateField(input_formats=('%d/%m/%Y', ""))

	class Meta:
		model = Transaction

class WalletTotalSerializer(serializers.Serializer):

	wallet = WalletSerializer()
	total = serializers.DecimalField(max_digits=12, decimal_places=4)
