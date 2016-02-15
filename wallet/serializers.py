from rest_framework import serializers

from wallet.models import Wallet, Item, Transaction, Category, Tag

class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		exclude = ('user', )

class TagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tag
		exclude = ('user', )

class ItemSerializer(serializers.ModelSerializer):

	category = CategorySerializer(read_only=True)
	category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
	tags = TagSerializer(many=True, read_only=True)
	tags_write = serializers.CharField(required=False, write_only=True, allow_blank=True)

	class Meta:
		model = Item
		exclude = ('pending',)

class WalletSerializer(serializers.ModelSerializer):

	class Meta:
		model = Wallet
		exclude = ('user',)

class TransactionSerializer(serializers.ModelSerializer):

	item = ItemSerializer()	
	wallet = WalletSerializer(read_only=True)
	wallet_id = serializers.IntegerField(write_only=True)
	date = serializers.DateField(input_formats=('%Y/%m/%d',))	

	class Meta:
		model = Transaction

	def create(self, validated_data):

		item_data = validated_data.pop('item')
		tags = self.check_tags(item_data.pop('tags_write'))
		item = Item.objects.create(**item_data)
		item.tags = tags
		item.save()

		wallet = Wallet.objects.get(pk=validated_data.pop('wallet_id'))

		transaction = Transaction.objects.create(item=item, wallet=wallet, date=validated_data.pop('date'))
		
		return transaction

	def update(self, instance, validated_data):
		item = instance.item

		item_data = validated_data.pop('item')
		item.amount = item_data.get('amount')
		item.note = item_data.get('note')
		item.category_id = item_data.get('category_id')	
		item.tags = self.check_tags(item_data['tags_write'])
		item.save()

		wallet = Wallet.objects.get(pk=validated_data.pop('wallet_id'))
		
		transaction = instance		
		transaction.wallet = wallet
		transaction.date = validated_data.get('date')

		transaction.save()
		
		return transaction

	def check_tags(self, tags):
		"""
		Check the tags and created if they don't exists
		"""
		if tags:
			tags_list = list()
			for t in tags.split(','):
				t = t.strip()
				if t:
					# check if tag exists
					try:
						t = Tag.objects.get(name=t)
					except Tag.DoesNotExist:
						# create the tag
						t = Tag.objects.create(name=t, user=self.context['request'].user)
					
					tags_list.append(t)

			return tags_list
		return list()

class TransactionsTotalSerializer(serializers.Serializer):
	
	total = serializers.DecimalField(max_digits=12, decimal_places=2)

class WalletTotalSerializer(serializers.Serializer):

	wallet = WalletSerializer()
	total = serializers.DecimalField(max_digits=12, decimal_places=4)

class GraphSeriesSerializer(serializers.Serializer):

	year_month = serializers.CharField()
	amount = serializers.DecimalField(max_digits=12, decimal_places=4) 
