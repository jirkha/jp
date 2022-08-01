from django import forms
from django.forms import ModelForm
from jp_app.models import ProductType, Product, Item, SaleType, Sale, Transaction
from jp_app.models import MaterialType, Material, Storage, Removal
from jp_app.models import Idea

import datetime
from datetime import date


###   PRODEJ   ###


# class CreateProduct(forms.Form):
#     name = forms.CharField(label="Jméno", max_length=256)  # název produktu
#     # typ produktu (svíčka / vonný vosk / difuzér atd.)
#     type = forms.CharField(label="Typ", max_length=128)
#     production_costs = forms.IntegerField(label="Výrobní náklady")  # výrobní náklady
#     selling_price = forms.IntegerField(label="Prodejní cena")  # prodejní cena

class ProductTypeForm(ModelForm):
    class Meta:
        model = ProductType
        fields = ["name"]

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "product_type", "items",
                  "jp_candles", "procedure", "note"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Název produktu'}),
            'product_type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'items': forms.SelectMultiple(attrs={'class': 'form-control form-control-sm chosen', 'size': 10}),
            'jp_candles': forms.NullBooleanSelect(attrs={'class': 'form-control form-control-sm'}),
            'procedure': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Zde přidejte postup výroby, recept apod.'}),
            'note': forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
        }
        
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "costs", "supplier", "link", "note"]
        labels = {
            'name': ('Položka'),
            'costs': ('Cena'),
            'supplier': ('Dodavatel'),
            'link': ('Odkaz'),
            'note': ('Poznámka'),
            }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Název položky', 'title': 'Your name'}),
            'costs': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Cena za položku (celkem)'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Název dodavatele položky (obchodu)'}),
            'link': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': "Odkaz na dodavatele (nutno zadat ve formátu 'www.dodavatel.cz')"}),
            'note': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 1, 'cols': 1, 'placeholder': 'Poznámka (volitelné)'}),
        }

class SaleTypeForm(ModelForm):
    class Meta:
        model = SaleType
        fields = ["name"]

class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ["name", "type", "jp_candles"]


class DateInput(forms.DateInput):
    input_type = 'date'


class TransactionForm(ModelForm):
    #day_of_sale = forms.DateField(widget=DateInput)
    #sales_channel = forms.ModelChoiceField(queryset=Sale.objects.filter(id=1))
    #product = forms.ModelChoiceField(queryset=Product.objects.filter(id=1))
    class Meta:
        model = Transaction
        fields = ["day_of_sale", "sales_channel",
                  "product", "product_price", "quantity_of_product"]
        widgets = {'day_of_sale': DateInput()}
        #fields = '__all__'



### slouží k filtrování prodaných položek dle data a následnému zobrazení v grafech
class SearchForm(forms.Form): 

    CHART_CHOICES = (
        ('Bar chart', 'Bar chart'),
        ('Pie chart', 'Pie chart'),
        ('Line chart', 'Line chart')
    )

    PERIOD_CHOICES = (
        ('Days', 'Dny'),
        ('Months', 'Měsíce'),
        ('Years', 'Roky')
    )

    date_from = forms.DateField(widget=DateInput)
    date_to = forms.DateField(widget=DateInput, initial=date.today)
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    period = forms.ChoiceField(choices=PERIOD_CHOICES)


###   SKLAD   ###


class MaterialTypeForm(ModelForm):
    class Meta:
        model = MaterialType
        fields = ["name"]


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ["name", "type"]


class StorageForm(ModelForm):
    class Meta:
        model = Storage
        fields = '__all__'
        widgets = {'day_of_storage': DateInput()}


class RemovalForm(ModelForm):
    class Meta:
        model = Removal
        fields = '__all__'
        widgets = {'day_of_removal': DateInput()}



###   NÁPADY   ###


class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Jméno'}),
            'product_type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'production_costs': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Výrobní náklady'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Prodejní cena'}),
            'introduction_day': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Select a date', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'note': forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
        }
