from django.contrib import admin
from wallet.models import Wallet, Transaction, Item, Category, Tag
# Register your models here.

admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Tag)