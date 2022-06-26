import django_filters
from .models import *


class TransactionFilter(django_filters.FilterSet):

    class Meta:
        model = Transaction
        # fields = '__all__'
        # func = django_filters.ModelMultipleChoiceFilter(
        #     field_name='product', queryset=Product.objects.all(), conjoined=True)
        fields = ["day_of_sale", "sales_channel",
                  "product", "product_price", "quantity_of_product", "created"]
