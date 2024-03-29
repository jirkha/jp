from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, FileResponse
from django.db.models import Sum, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from collections import Counter

from .models import ProductType, Product, Item, SaleType, Sale, Transaction
from .models import MaterialType, Material, Storage, Removal
from .models import Idea

from .forms import ProductTypeForm, ProductForm, ItemForm, SaleTypeForm, SaleForm, TransactionForm, SearchForm
from .forms import MaterialTypeForm, MaterialForm, StorageForm, RemovalForm
from .forms import IdeaForm

from .filters import TransactionFilter

from .utils import (
    get_sales_channel_from_id,
    get_product_from_id, 
    get_chart_price,
    get_json,
)
    
import datetime
import pandas as pd
import json

### google drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

### pdf creator
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa


###   PRODEJ   ###



### zobrazí seznam všech produktů, i když zadám konkrétní "id"
def index(response, id):
    p = Product.objects.get(id=id)
    return render(response, "jp_app/list.html", {})

### zobrazí domovskou stránku (aktuálně bez obsahu)
def home(response):
    return render(response, "jp_app/home.html", {})


class ProductView(ListView):
    model = Product
    template_name = 'jp_app/product/product.html'
    ordering = ['-created']  # seřadí seznam produktů sestupně dle "data vložení"
    paginate_by = 15 ### pokud bude mít seznam více než  15 položek, rozdělí se v teplate na více stránek
    
    ### fce "get_context_data" umožňuje upravovat a přidávat pole/hodnoty v následně zobrazené template u class Views (v tomto případě ListView)
    ### v tomto případě fce spočítá celkové výrobní náklady z jednotlivých položek "items" obsažených/přiřazených danému produktu
    def get_context_data(self, **kwargs):
        ### "context" předdefinovaný (neměnit)
        context = super(ProductView, self).get_context_data(**kwargs)
        ### prochází postupně všechny produkty
        for p in Product.objects.all(): 
            i_sum=0
            ### prochází a postupně ukládá ceny ("costs") všech "items" obsažených v daném produktu
            for i in p.items.values('costs'):
                i_sum += i['costs']
            ### uloží do pole "production_costs" daného produktu celkovou částku za všechny "items" a tím vypočítá výrobní náklady daného produktu
            p.production_costs = i_sum
            p.save()
        ### "context" umožní zobrazení nově upraveného pole "production_costs" v template 'jp_app/product/product.html'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'jp_app/product/product-detail.html'


### automaticky (pomocí CreateView) načte formulář sloužící k vložení produktů
class CreateProduct(SuccessMessageMixin, CreateView):
    ### "SuccessMessageMixin" slouží k tomu, aby se po vložení produktu a přesměrování na seznam produktů (k tomu slouží atribut "success_url") mohlo zobrazit potvrzení uložení
    model = Product  # models.py
    form_class = ProductForm  # forms.py
    # pokud kvůli bootstrap mám "template_name", musím zakomentovat "fields"
    template_name = 'jp_app/product/product_add.html'
    # template_name = 'jp_app/idea_add.html'
    # fields = '__all__'
    success_url = reverse_lazy('jp_app:product') ### po uložení produktu přesměruje na stránku se seznamem produktů
    success_message = "Produkt %(name)s byl úspěšně uložen" ### po vložení zobrazí upozornění
    

class UpdateProduct(UpdateView):
    model = Product
    form_class = ProductForm  # forms.py
    # pokud kvůli bootstrap mám "template_name", musím zakomentovat "fields"
    template_name = 'jp_app/product/product_update.html'
    # fields = '__all__'


class DeleteProduct(DeleteView):
    model = Product
    template_name = 'jp_app/product/product_delete.html'
    # 'reverse_lazy' slouží k určení stránky, na kterou po smazání nápadu bude přesměrováno
    success_url = reverse_lazy('jp_app:product')


### vytvoří a zobrazí seznam "items", tzn. jednotlivých položek, ze kterých se skládají produkty
def item(response):
    i = Item.objects.all()
    i_count = i.count()  ### fce počítá součet vložené typy produktů
    form_i = ItemForm()
    
    if response.method == "POST":
        if "save_i" in response.POST: 
            form_i = ItemForm(response.POST)
            if form_i.is_valid():
                form_i.save()
        if response.POST.get("delete_i"):
            # převede QueryDict na dictionary "id" položky, kterou chceme smazat
            x = response.POST.dict()['delete_i']
            # vyhledá odpovídající transakci (dle id=x)
            z = Item.objects.get(id=x)
            z.delete()  # vymaže danou položku naskladnění
            messages.success(response, ('Item byla úspěšně vymazán'))
    
    
    dict = {
        "i": i,
        "i_count": i_count,
        "form_i": form_i,
      }

    return render(response, "jp_app/product/item.html", dict)


### umožní editovat objekt "item"
def item_update(response, id):
    item = Item.objects.get(id=id)
    form = ItemForm(response.POST or None,
                    instance=item)
    if form.is_valid():
        form.save()
        messages.success(response, ('Item byla úspěšně změněna'))
        return redirect("/item")
    
    dict = {
        "form": form,
        "item": item,
    }
    
    return render(response, "jp_app/product/item_update.html", dict)



### zobrazí všechny položky kategorie prodej ###
def list(response):
    pt = ProductType.objects.all()
    p = Product.objects.all()
    st = SaleType.objects.all()
    s = Sale.objects.all()
    t = Transaction.objects.all()

    ### slouží k vymazání dané transakce ###
    if response.method == "POST":
        ### aktivace tlačítkem "delete" u příslušné transakce
        if response.POST.get("delete_t"):
            # převede QueryDict na dictionary "id" položky, kterou chceme smazat
            x = response.POST.dict()['delete_t']
            # vyhledá odpovídající transakci (dle id=x)
            z = Transaction.objects.get(id=x)
            z.delete()  # vymaže danou položku naskladnění
            messages.success(response, ('Transakce byla úspěšně vymazána'))
    
    ### další část kód slouží k výpočtu tržeb po jednotlivých dnech ###
    q = Transaction.objects.values('day_of_sale').distinct() ### uloží unikátní dny, ve kterých se uskutečnila transakce (class Transaction)
    #print(q)
    tt = []
    temp1 = 0
    total = 0
    for date in q: ### prochází postupně všechny dny, kdy se uskutečnila transakce
        t1 = Transaction.objects.filter(day_of_sale=date["day_of_sale"]) ### uloží konkrétní den dané iterace cyklu "for"
        #print(t1)
        #print(len(t1))
        temp = 0
        lst = []
        for x in range(len(t1)): ### prochází postupně všechny transakce daného dne
            #print(x)
            temp += (t1[x]).total_price  ### uloží utrženou částku za danou transakci
            
        ### We can use (*) operator to get all the values of the dictionary in a list
        temp_value = [*(q[temp1]).values()][0] ### uloží hodnotu data aktuální iterace (* a fce values slouží k očištění daného data, aby nebylo zabaleno v listu a dalo se dále uložit)
        lst.extend([temp_value, temp])  # přidá do dočasného listu datum z temp_value spolu s utrženou částkou v daném dni (fce"extend" je alternativou k "append" a slouží k vložení více hodnot do listu najdednou)
        #print(lst)
        tt.append(lst) ### vloží hodnoty z dočasného listu "lst" do finálního souhrnného listu "tt", který obsahuje všechny potřebného hodnoty pro výpis tržeb
        total += temp ### počítá celkovou utrženou částku za všechny transakce
        temp1 += 1
    #print(tt)


    ### vypočte, kolik bylo prodáno ks jednotlivých výrobků (z uskutečněných transakcí) ###
    id_p = Product.objects.values('id')
    ### prochází jednotlivé výrobky dle "id"
    for product in id_p:
        # print("id_p:", id_p)
        # print("product['id']:", product['id'])
        ### z trasakcí seskupených dle "id" prodaného výrobku vypočte celkový počet prodaných ks daného výrobku
        y = Transaction.objects.filter(product__id=product['id']).values(
            'product').annotate(sum=Sum('quantity_of_product')).values('sum')
        ### "z1" je list_comprehension, jehož výsledkem je ale list, proto se zatám nepoužívá a místo toho je níže "for z in y", které z QuerySetu vyndá počet prodaných výrobků pro další použití
        # z1 = ([z['sum'] for z in y])
        # print("z1:",z1)
        for z in y:
            ### najde produkt, který je aktuálně součástí daného cyklu "for product in id_p"
            pr1 = Product.objects.get(id=product['id'])
            ### k danému atributu "sold" daného produktu přiřadí počet prodaných ks a uloží ho
            pr1.sold = z['sum']
            pr1.save()

    print(t.values('day_of_sale'))
    
    ### tato část slouží k filtrování transakcí ###
    myFilter = TransactionFilter(response.GET, queryset=t) 
    t = myFilter.qs
    #print(t)

    ### fce počítá součet vložené typy produktů ###
    pt_count = pt.count()


    
    dict = {
        "pt": pt,
        "p": p,
        "st": st,
        "s": s,
        "t": t,
        "q": q,
        "myFilter": myFilter,
        "pt_count": pt_count,
        "tt": tt,  ### obsahuje všechny potřebného hodnoty pro výpis tržeb
        "total": total,  ### celková utržená částka za všechny transakce
         }
    
    return render(response, "jp_app/list.html", dict)

### umožňuje vkládat všechny položky kategorie prodej
def create(response):
    # form = CreateProduct()
    # response.user
    form_pt = ProductTypeForm()
    form_p = ProductForm()
    form_st = SaleTypeForm()
    form_s = SaleForm()
    form_t = TransactionForm()
    
    dict = {"form_pt": form_pt, "form_p": form_p, "form_st": form_st, "form_s": form_s, "form_t": form_t}
    if response.method == "POST":
        if "save_p" in response.POST: ### produkt
            form_p = ProductForm(response.POST)
            if form_p.is_valid():
                form_p.save()
        elif "save_pt" in response.POST: ### typ produktu
            form_pt = ProductTypeForm(response.POST)
            if form_pt.is_valid():
                # print(response.POST)
                form_pt.save()
        elif "save_st" in response.POST:  # prodejní kanál
            form_st = SaleTypeForm(response.POST)
            if form_st.is_valid():
                # print(response.POST)
                form_st.save()
        elif "save_s" in response.POST:  # prodejní kanál
            form_s = SaleForm(response.POST)
            if form_s.is_valid():
                # print(response.POST)
                form_s.save()
        elif "save_t" in response.POST: ### transakce
            form_t = TransactionForm(response.POST)
            #d = form_t.cleaned_data["day_of_sale"]
            #s = form_t.cleaned_data["sales_channel"]
            #p = form_t.cleaned_data["product"]
            s = response.POST.dict()['sales_channel']
            p = response.POST.dict()['product']
            t = form_t.cleaned_data["day_of_sale"]
            q = form_t.cleaned_data["quantity_of_product"]
            sp = form_t.cleaned_data["product_price"]
             
            # #trans = Transaction(sales_channel=s, product=p, quantity_of_product=q)
            # print(s)
            # print(p)
            # print(t)
            # print(q)
            # y = {"day": t, "products": {p: q}}
            # print(y)
            # sale = Sale.objects.get(id=s)
            # temp1 = sale.sold
            # print(sale)
            # print(temp1)
            # if y["day"] in temp1:
            #     pass


            # y = Material.objects.get(id=x)
            # temp1 = y.quantity_of_material
            # temp2 = y.price
            # y.quantity_of_material = temp1 + q
            # y.price = temp2 + p
            # y.save()

            if form_t.is_valid():
                print("valid")
                form_t.save()
        else:
            pass

    return render(response, "jp_app/create.html", dict) ### po uložení produktu se znovu objeví stránka s formuláři




###   SKLAD   ###


### zobrazí všechny položky kategorie sklad
def list_material(response):
    mt = MaterialType.objects.all()
    m = Material.objects.all()
    st = Storage.objects.all()
    r = Removal.objects.all()

    mt_count = mt.count() ### počet položek typ materiálu
    m_count = m.count()  ### počet položek materiál

    if response.method == "POST":
        # print(response.POST)
        ### aktivace tlačítkem "delete" u příslušného naskladnění
        if response.POST.get("delete_st"): 
            x = response.POST.dict()['delete_st']  ### převede QueryDict na dictionary "id" položky, kterou chceme smazat
            # print(x)
            z = Storage.objects.get(id=x) ### vyhledá odpovídající položku naskladnění (dle id=x)
            # print(z)
            temp1 = z.quantity_of_material ### dočasně uloží podrobnosti dané položky naskladnění
            temp2 = z.price
            temp3 = z.material_id
            y = Material.objects.get(id=temp3) ### vyhledá příslušný materiál, jehož část chceme ze skladových zásob vymazat
            # print(temp1)
            # print(temp2)
            # print(y)
            temp4 = y.quantity_of_material ### vyhledá množství materiálu, jehož část chceme ze skladových zásob vymazat
            temp5 = y.price
            y.quantity_of_material = temp4 - temp1 ### od aktuálního množství daného materiálu odečte množství, které bylo u dané položky naskladnění, jež vymazáváme
            y.price = temp5 - temp2
            y.save() ### uloží aktualizované množství daného materiálu ve skladu
            z.delete() ### vymaže danou položku naskladnění

        ### aktivace tlačítkem "delete" u příslušného vyskladnění
        elif response.POST.get("delete_r"):
            # print(response.POST)
            x = response.POST.dict()['delete_r']
            # print(x)
            z = Removal.objects.get(id=x)
            # print(z)
            temp1 = z.quantity_of_material
            # temp2 = z.price
            temp3 = z.material_id
            y = Material.objects.get(id=temp3)
            # print(temp1)
            # print(temp2)
            # print(y)
            temp4 = y.quantity_of_material
            # temp5 = y.price
            y.quantity_of_material = temp4 + temp1
            # y.price = temp5 + temp2
            y.save()
            z.delete()
    
    # st_dict={}
    # for id in range(1,(len(m))+1):
    #     stx = Storage.objects.filter(material_id=id).aggregate(id=Sum('quantity_of_material'))
    #     stx=stx['id']
    #     st_dict[Material.objects.get(id=id).name] = stx
    # print(st_dict)
    
    dict = {
        "mt": mt, "m": m, "st": st, "r": r, "mt_count": mt_count, "m_count": m_count,# "st_dict": st_dict
        }
    return render(response, "jp_app/list_material.html", dict) ### po uložení produktu se znovu objeví stránka s formuláři

### umožňuje vkládat všechny položky kategorie sklad
def material(response):
    form_mt = MaterialTypeForm()
    form_m = MaterialForm()
    form_st = StorageForm()
    form_r = RemovalForm()

    if response.method == "POST":
        if "save_mt" in response.POST: ### typ skladové položky (materiálu)
            form_mt = MaterialTypeForm(response.POST)
            if form_mt.is_valid():
                form_mt.save()
        elif "save_m" in response.POST: ### materiál
            form_m = MaterialForm(response.POST)
            if form_m.is_valid():
                form_m.save()
        elif "save_st" in response.POST: ### naskladnění
            form_st = StorageForm(response.POST)
            if form_st.is_valid():
                form_st.save()
                ### další kód slouží k úpravě celkového aktuálního stavu skladu (navýšení)
                q = form_st.cleaned_data["quantity_of_material"] ### "cleaned_data" očistí hodnotu formulářového pole
                p = form_st.cleaned_data["price"]
                x = response.POST.dict()['material']
                y = Material.objects.get(id=x)
                temp1 = y.quantity_of_material
                temp2 = y.price
                y.quantity_of_material = temp1 + q
                y.price = temp2 + p
                y.save()

        elif "save_r" in response.POST: ### vyskladnění
            form_r = RemovalForm(response.POST)
            if form_r.is_valid():
                form_r.save()
                ### další kód slouží k úpravě celkového aktuálního stavu skladu (snížení)
                q = form_r.cleaned_data["quantity_of_material"]
                # p = form_r.cleaned_data["price"]
                x = response.POST.dict()['material'] ### převede QueryDict na dictionary "id" položky, kterou chceme editovat
                y = Material.objects.get(id=x)
                temp1 = y.quantity_of_material
                # temp2 = y.price
                y.quantity_of_material = q - temp1
                # y.price = p - temp2
                y.save()

        else:
            pass
    
    dict = {"form_mt": form_mt, "form_m": form_m,
            "form_st": form_st, "form_r": form_r}

    return render(response, "jp_app/material.html", dict)




### STATISTIKY A GRAFY ###

today = datetime.date.today()

### Statistiky skladu ###
def material_chart(response):
    # template = "jp_app/charts.html"
    # return render(response, template)
    # transaction = Transaction.objects.filter(
    #     ["product", "day_of_sale"]).values_list()

    t = Transaction.objects.all()
    #mt = MaterialType.objects.all()
    m = Material.objects.all()
    #st = Storage.objects.all()
    #r = Removal.objects.all()

    
    ### další část kód slouží k výpočtu tržeb po jednotlivých dnech ###
    # uloží unikátní dny, ve kterých se uskutečnila transakce (class Transaction)
    q = Transaction.objects.values('day_of_sale').distinct()
    #print(q)
    global tt
    tt = []
    temp1 = 0
    total = 0
    for date in q:  # prochází postupně všechny dny, kdy se uskutečnila transakce
        # uloží konkrétní den dané iterace cyklu "for"
        t1 = Transaction.objects.filter(day_of_sale=date["day_of_sale"])
        #print(t1)
        #print(len(t1))
        temp = 0
        lst = []
        for x in range(len(t1)):  # prochází postupně všechny transakce daného dne
            #print(x)
            # uloží utrženou částku za danou transakci
            temp += (t1[x]).total_price
            #print(temp)
            

        ### We can use (*) operator to get all the values of the dictionary in a list
        # uloží hodnotu data aktuální iterace (* a fce values slouží k očištění daného data, aby nebylo zabaleno v listu a dalo se dále uložit)
        temp_value = [*(q[temp1]).values()][0]
        # přidá do dočasného listu datum z temp_value spolu s utrženou částkou v daném dni (fce"extend" je alternativou k "append" a slouží k vložení více hodnot do listu najdednou)
        lst.extend([temp_value, temp])
        #print(lst)
        # vloží hodnoty z dočasného listu "lst" do finálního souhrnného listu "tt", který obsahuje všechny potřebného hodnoty pro výpis tržeb
        tt.append(lst)
        total += temp  # počítá celkovou utrženou částku za všechny transakce
        temp1 += 1

    tt.sort() ### seřadí list podle datumů vzestupně
    print(tt)
    
    #mt_count = mt.count()  # počet položek typ materiálu
    m_count = m.count()  # počet položek materiál
    
    dict = {"t": t, "m": m, "m_count": m_count, "tt":tt}
    return render(response, "jp_app/mat-chart.html", dict)


### Statistiky a graf s filtrem (využití pandas a matplotlib) ###
### funkci využívá i fce "stat_chart" pro zobrazení denních, měsíčních a ročních statistik
### atribut "view=None" se využívá pro účely rozpoznání vyvolatele funkce -> pokud je funkce vyvolána fcí "stat_chart", atribut se změní z None na stat_chart
def statistic(response, view=None):
    global df_d
    df_d = 0
    global df_m
    df_m = 0
    global df_y
    df_y = 0

    form_stat = SearchForm(response.POST or None)
    date_from = datetime.date(2021,1,1)
    date_to = today
    qs_tr = None
    period = "Months"
    chart_type = 'Bar chart'

    if response.method == "POST":
        date_from = response.POST.get('date_from')
        date_to = response.POST.get('date_to')
        chart_type = response.POST.get('chart_type')
        period = response.POST.get('period')

    qs_tr = Transaction.objects.filter(
        day_of_sale__lte=date_to, day_of_sale__gte=date_from)
    df_tr = pd.DataFrame(qs_tr.values())

    if len(qs_tr) > 0:
        df_tr["sales_channel_id"] = df_tr["sales_channel_id"].apply(get_sales_channel_from_id) ### za pomoci funkce v souboru utils.py vymění v DataFrame u prodejního kanálu id za název
        df_tr["product_id"] = df_tr["product_id"].apply(
            get_product_from_id)  ### za pomoci funkce v souboru utils.py vymění v DataFrame u produktu id za název
        # df_tr["day_of_sale"] = df_tr["day_of_sale"].apply(
        #     lambda x: x.strftime('%a %d.%m.%Y')) ### změní formát data v DataFrame
        df_tr["created"] = df_tr["created"].apply(
            lambda x: x.strftime('%d.%m.%Y'))  ### změní formát data v DataFrame
            
        df_tr.rename({   ### přejmenuje názvy vybraných sloupců v DataFrame
            "sales_channel_id": "sales_channel",
            "product_id": "produkt",
        },
            axis = 1,
            inplace = True
        )  
        ### axis=1 vyjadřuje, že se pracuje se sloupcem (axis=0 by bylo v případě řádků)
        ### inplace=True změní v DataFrame dané hodnoty a uloží nový stav

    df_d = df_tr.groupby('day_of_sale', as_index=False)['total_price'].agg('sum') ### vytvoří DataFrame s celkovými tržbami v jednotlivých dnech
    #df_d = df_d.style.highlight_max(color='red')
    #df_d = df_d.style.hide_index()
    print('df_d: ',df_d)
    
    ### TVORBA SUMÁŘE TRŽEB DLE MĚSÍCŮ A LET ###
    ### vytvoří nový DataFrame a nastaví správný formát datumů u hodnot ve sloupci "day_of_sale" a umístí ho do indexu tabulky (pro účely dalšího zpracování dat)
    df_m = df_d.set_index(pd.DatetimeIndex(df_d['day_of_sale']), drop=False)
    ### vytvoří nový DataFrame se součtem tržeb dle jednotlivých let
    df_y = df_m.groupby(df_m.index.year.values).sum()
    ### resetuje index -> z indexu obsahující údaj o roku udělá sloupec s názvem "index", jehož údaj se následně bude zobrazovat
    df_y = df_y.reset_index()
    ### seskupí DataFrame dle jednotlivých měsíců a sečte celkové tržby za daný měsíc
    df_m = df_m.groupby([df_m.index.year, df_m.index.month]).sum()
    ### přejmenuje indexy, aby se s nimi dalo dále pracovat
    df_m.index.names = ["year_of_sale","month_of_sale"] 
    ### přejmenuje sloupce a z indexů "year_of_sale" a "month_of_sale" udělá sloupce, z jejichž dat se následně zobrazí číslo daného měsíce a rok
    df_m = df_m.rename(columns={'day_of_sale': 'day'}).reset_index()
    ### vytvoří nový sloupec se spojeným měsícem a rokem (funkce "str.cat") převedeným na string (funkce "apply") a odděleným "/" (sep="/")
    df_m['month_year'] = df_m['month_of_sale'].apply(str).str.cat(df_m['year_of_sale'].apply(str), sep="/")
    ### přeskupí pořadí sloupců, aby byl sloupec 'month_year' jako první pro sjednocení prvního sloupce u df_m/d/y pro účely zobrazení v grafu
    df_m = df_m[['month_year', 'month_of_sale', 'year_of_sale', 'total_price']]
    
    ### automaticky zobrazí graf s tržbami po jednotlivých dnech (pokud není funkce vyvolána funkcí "stat_chart", kdy to není třeba)
    if view != 'stat_chart':
        chart = get_chart_price(chart_type, df_d, labels=df_d['day_of_sale'].values)

    ### zobrazí konkrétní typ grafu dle požadavku z formuláře, pokud je zadán
    if response.method == "POST":
        if "Days" in response.POST['period']:
            #print("response.POST['period']: ", response.POST['period'])
            chart = get_chart_price(
                chart_type, df_d, labels=df_d['day_of_sale'].values)
        elif "Months" in response.POST['period']:
            #print("response.POST['period']: ", response.POST['period'])
            chart = get_chart_price(
                chart_type, df_m, labels=df_m['month_year'].values)
        elif "Years" in response.POST['period']:
            #print("response.POST['period']: ", response.POST['period'])
            chart = get_chart_price(
                chart_type, df_y, labels=df_y['index'].values)

    ### sloužilo pro zobrazení tabulek ve formě html, nyní již není třeba, protže se využívá json s ohledem na lepší grafické zobrazení
    #df_tr = df_tr.to_html()
    #df_d = df_d.to_html()
    #df_m = df_m.to_html()
    #df_y = df_y.to_html()
    
    ### json_records_x vyvolá funkci v unit.py, která nastaví správný výstupní fpormát čas (Json)
    json_records_d = get_json(df_d)
    json_records_m = get_json(df_m)
    json_records_y = get_json(df_y)

    # print("json_records_d:", json_records_d)
    # print("json_records_m:", json_records_m)
    # print("json_records_y:", json_records_y)
    
    df_m = []
    df_m = json.loads(json_records_m)
    df_d = []
    df_d = json.loads(json_records_d)
    df_y = []
    df_y = json.loads(json_records_y)

    ### v případě chodu funkce vyvolané "stat_chart" ukončí průběh funkce a odešle do fce "stat_chart" data
    if view == 'stat_chart':
        return df_d, df_m, df_y


    dict = {
        "form_stat": form_stat,
        "df_d": df_d,
        "df_m": df_m,
        "df_y": df_y,
        "chart": chart,
    }
    return render(response, "jp_app/statistic.html", dict)


### Statistiky s grafy (využití předchozí funkce "statistic" a chart.js) ###
def stat_chart(response):
    ### proměnná "a" vyvolá fci "statistic", ze které získá požadované statistiky pro účely jejich zobrazení a vykreslení v grafu na stránce "stat_chart.html"
    a = statistic(response, 'stat_chart')

    # print('df_d:', df_d)
    # print('df_m:', df_m)
    # print('df_y:', df_y)

    dict = {
        "df_d": df_d,
        "df_m": df_m,
        "df_y": df_y,
    }
    return render(response, "jp_app/stat_chart.html", dict)
    




###   NÁPADY   ###


### automaticky (pomocí ListView) načte seznam nápadů vložených pomocí "CreateIdea"
### jednodušší alternativa k řešení pomocí funkcí (viz výše)
class IdeaView(ListView):
    model = Idea
    template_name = 'jp_app/idea/idea.html'
    ordering = ['-created']  # seřadí seznam nápadů sestupně dle "data vložení"

    # ### slouží k sečtení celkového počtu vložených položek "nápady" a následnému zobrazení na stránce
    # def idea(self, response):
    #     i = Idea.objects.all()

    #     i_count = i.count()
    #     print(i_count)

    #     dict = {
    #         "i_count": i_count,
    #     }
    #     return render(response, "jp_app/idea/idea.html", dict)

### zobrazí stránku s detailem dané položky "nápad" (url: "/idea/<id>", template: "idea.detail.html")


class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'jp_app/idea/idea-detail.html'

### automaticky (pomocí CreateView) načte formulář sloužící k vložení nápadů


class CreateIdea(CreateView):
    model = Idea  # models.py
    form_class = IdeaForm  # forms.py
    # pokud kvůli bootstrap mám "template_name", musím zakomentovat "fields"
    template_name = 'jp_app/idea/idea_add.html'
    # template_name = 'jp_app/idea_add.html'
    # fields = '__all__'


class UpdateIdea(UpdateView):
    model = Idea
    form_class = IdeaForm  # forms.py
    # pokud kvůli bootstrap mám "template_name", musím zakomentovat "fields"
    template_name = 'jp_app/idea/idea_update.html'
    # fields = '__all__'


class DeleteIdea(DeleteView):
    model = Idea
    template_name = 'jp_app/idea/idea_delete.html'
    # 'reverse_lazy' slouží k určení stránky, na kterou po smazání nápadu bude přesměrováno
    success_url = reverse_lazy('jp_app:idea')





### GOOGLE ###



def google(response):
    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()
    drive = GoogleDrive(g_login)
    
    # # to check the current working directory, if the current working directory above is different than your folder containing the script then change the working directory to your script directory.
    # print(os.getcwd())

    # file = drive.CreateFile({'title': 'My Awesome File.txt'})
    # # this writes a string directly to a file
    # file.SetContentString('Hello World!')
    # # SetContentFile( název souboru ) => alternativa ke "SetContentString", která jako obsah vloží obsah jiného souboru
    # file.Upload()
    
    dict = {}
    return render(response, "jp_app/google.html", dict)




### PDF ####

### https://thecodelearners.com/django-tutorial-on-pdf-generation-and-rendering-with-xhtml2pdf-package/
def render_pdf(request):
    path = "jp_app/pdf/pdf_template.html"
    print(path)
    context = {"product": Product.objects.all()[:100]}

    html = render_to_string('jp_app/pdf/pdf_template.html', context)
    #html = render_to_string('templates/jp_app/pdf/pdf_template', context)
    io_bytes = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
    response = HttpResponse(io_bytes.getvalue(),
                            content_type='application/jp_app')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    if not pdf.err:
        return response
    else:
        return HttpResponse("Error while rendering PDF", status=400)

