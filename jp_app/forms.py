from django import forms
from django.forms import ModelForm
from jp_app.models import ProductType, Product, SaleType, Sale, Transaction
from jp_app.models import MaterialType, Material, Storage, Removal
from jp_app.models import Idea


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
        fields = ["name", "product_type", "production_costs", "jp_candles"]

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
                  "product", "selling_price", "quantity_of_product"]
        widgets = {'day_of_sale': DateInput()}
        #fields = '__all__'


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
            'introduction_day': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'rrrr-mm-dd'}),
            'status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'note': forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
        }
