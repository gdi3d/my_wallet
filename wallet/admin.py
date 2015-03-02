from django.contrib import admin
from wallet.models import Wallet, Transaction, FavoriteItem, Item, Category
# Register your models here.

admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(FavoriteItem)
admin.site.register(Item)
admin.site.register(Category)