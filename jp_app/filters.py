import django_filters
from .models import *


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        # fields = '__all__'
        fields = ["day_of_sale", "sales_channel",
                  "product", "selling_price", "quantity_of_product", "created"]
