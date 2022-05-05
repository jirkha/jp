from django import forms
from django.forms import ModelForm
from jp_app.models import Product, Sale, Transaction

# class CreateProduct(forms.Form):
#     name = forms.CharField(label="Jméno", max_length=256)  # název produktu
#     # typ produktu (svíčka / vonný vosk / difuzér atd.)
#     type = forms.CharField(label="Typ", max_length=128)
#     production_costs = forms.IntegerField(label="Výrobní náklady")  # výrobní náklady
#     selling_price = forms.IntegerField(label="Prodejní cena")  # prodejní cena

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "type", "production_costs", "selling_price"]


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ["name", "type", "jp_candles"]


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ["day_of_sale", "sales_channel",
                  "product", "quantity_of_product"]
