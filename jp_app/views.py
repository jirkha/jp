from django import forms
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
    dict = {"p": p, "s": s, "t": t}
    return render(response, "jp_app/list.html", dict)

def create(response):
    # form = CreateProduct()
    # response.user
    form_p = ProductForm()
    form_s = SaleForm()
    form_t = TransactionForm()
    dict = {"form_p": form_p, "form_s": form_s, "form_t": form_t}
    if response.method == "POST":
        if "save_p" in response.POST:
            form_p = ProductForm(response.POST)
            if form_p.is_valid():
                form_p.save()
        elif "save_s" in response.POST:
            form_s = SaleForm(response.POST)
            if form_s.is_valid():
                print(response.POST)
                form_s.save()
        elif "save_t" in response.POST:
            
            form_t = TransactionForm(response.POST)
            print(form_t.is_valid())
            #d = form_t.cleaned_data["day_of_sale"]
            #s = form_t.cleaned_data["sales_channel"]
            #p = form_t.cleaned_data["product"]
            #q = form_t.cleaned_data["quantity_of_product"]
            #trans = Transaction(sales_channel=s, product=p, quantity_of_product=q)
            #print(trans)
            #print(d)
            if form_t.is_valid():
                print("valid")
                form_t.save()
            
        else:
            pass

    return render(response, "jp_app/create.html", dict)


