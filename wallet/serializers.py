from rest_framework import serializers

from wallet.models import Wallet, Item, Transaction, Category, FavoriteItem

class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		exclude = ('user', )

class ItemSerializer(serializers.ModelSerializer):

	category = CategorySerializer(read_only=True)
	category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)	

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

	item = ItemSerializer()	
	wallet = WalletSerializer(read_only=True)
	wallet_id = serializers.IntegerField(write_only=True)
	date = serializers.DateField(input_formats=('%Y/%m/%d', ""))	

	class Meta:
		model = Transaction

	def create(self, validated_data):

		item_data = validated_data.pop('item')
		item = Item.objects.create(**item_data)

		wallet = Wallet.objects.get(pk=validated_data.pop('wallet_id'))

		transaction = Transaction.objects.create(item=item, wallet=wallet)       
		
		return transaction

	def update(self, instance, validated_data):

		item = instance.item

		item_data = validated_data.pop('item')
		item.amount = item_data.get('amount')
		item.note = item_data.get('note')
		item.category_id = item_data.get('category_id')
		item.save()

		wallet = Wallet.objects.get(pk=validated_data.pop('wallet_id'))
		
		transaction = instance		
		transaction.wallet = wallet
		transaction.date = validated_data.get('date')

		transaction.save()
		
		return transaction

class TransactionsTotalSerializer(serializers.Serializer):
	
	total = serializers.DecimalField(max_digits=12, decimal_places=2)

class WalletTotalSerializer(serializers.Serializer):

	wallet = WalletSerializer()
	total = serializers.DecimalField(max_digits=12, decimal_places=4)
