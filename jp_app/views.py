from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Sale, Transaction
from .forms import ProductForm, SaleForm, TransactionForm
# Create your views here.

def index(response, id):
    p = Product.objects.get(id=id)
    return render(response, "jp_app/list.html", {})

def home(response):
    return render(response, "jp_app/home.html", {})

def list(response):
    p = Product.objects.all()
    s = Sale.objects.all()
    t = Transaction.objects.all()
    dict = {"p": p, "s": s}
    return render(response, "jp_app/list.html", dict)

def create(response):
    # form = CreateProduct()
    form_p = ProductForm()
    form_s = SaleForm()
    form_t = TransactionForm()
    dict = {"form_p": form_p, "form_s": form_s, "form_t": form_t}
    return render(response, "jp_app/create.html", dict)
