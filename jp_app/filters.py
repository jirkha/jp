import django_filters
from django import forms
from .models import *

import datetime
from datetime import date


class DateInput(forms.DateInput):
    input_type = 'date'


class TransactionFilter(django_filters.FilterSet):
    day_of_sale = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'})) # umožní vyhledávat datum pomocí kalendáře
    created = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}))  # umožní vyhledávat datum pomocí kalendáře
    class Meta:
        model = Transaction
        # fields = '__all__'
        # func = django_filters.ModelMultipleChoiceFilter(
        #     field_name='product', queryset=Product.objects.all(), conjoined=True)
        fields = ["day_of_sale", "sales_channel",
                  "product", "product_price", "quantity_of_product", "created"]
        widgets = {'day_of_sale': DateInput()}
