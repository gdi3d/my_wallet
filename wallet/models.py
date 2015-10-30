from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

import datetime

# Create your models here.
class Category(models.Model):

	user = models.ForeignKey(User)
	name = models.CharField('name', max_length=90)

	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")

	def __str__(self):
		return self.name
	
class Wallet(models.Model):

	user = models.ForeignKey(User)
	name = models.CharField(max_length=255)
	initial_amount = models.DecimalField(_('Initial Amount'), max_digits=12, decimal_places=4, default=0)
	note = models.TextField(blank=True, null=True)

	class Meta:
		verbose_name = "Wallet"        
		verbose_name_plural = "Wallets"

	def __str__(self):
		return self.name

class Tag(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(_('Name'), max_length=75)

	def __unicode__(self):
		return self.name

class AbstractItem(models.Model):
	amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=4)
	note = models.TextField(blank=True)
	pending = models.BooleanField(default=False)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
	tags = models.ManyToManyField(Tag, related_name='item_tags', blank=True)

	class Meta:
		abstract = True

	def __str__(self):
		return '$ %s (%s)' % (self.amount, self.category)

class Item(AbstractItem):

	class Meta:
		verbose_name = _("Item")
		verbose_name_plural = _("Items")	

class Transaction(models.Model):

	wallet = models.ForeignKey(Wallet)
	item = models.ForeignKey(Item)
	date = models.DateField(default=datetime.date.today, blank=False)

	class Meta:
		verbose_name = _("Transaction")
		verbose_name_plural = _("Transactions")

	def __str__(self):
		return '$ %s (%s)' % (self.item.amount, self.item.category)


class WalletHistory(object):
	pass