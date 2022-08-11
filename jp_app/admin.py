from django.contrib import admin
from .models import ProductType, Product, Item, SaleType, Sale, Transaction
from .models import MaterialType, Material, Storage, Removal
from .models import Idea

# Register your models here.

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Transaction)
admin.site.register(ProductType)
admin.site.register(Item)
admin.site.register(SaleType)
admin.site.register(MaterialType)
admin.site.register(Material)
admin.site.register(Storage)
admin.site.register(Removal)
admin.site.register(Idea)
