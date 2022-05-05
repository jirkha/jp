from django.contrib import admin
from .models import Product, Sale, Transaction

# Register your models here.

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Transaction)
