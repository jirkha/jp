from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import ProductType, Product, Sale, Transaction
from .models import MaterialType, Material, Storage, Removal
from .models import Idea

from .forms import ProductTypeForm, ProductForm, SaleForm, TransactionForm
from .forms import MaterialTypeForm, MaterialForm, StorageForm, RemovalForm
from .forms import IdeaForm

from .filters import TransactionFilter




###   PRODEJ   ###



### zobrazí seznam všech produktů, i když zadám konkrétní "id"
def index(response, id):
    p = Product.objects.get(id=id)
    return render(response, "jp_app/list.html", {})

### zobrazí domovskou stránku (aktuálně bez obsahu)
def home(response):
    return render(response, "jp_app/home.html", {})

### zobrazí všechny položky kategorie prodej
def list(response):
    pt = ProductType.objects.all()
    p = Product.objects.all()
    s = Sale.objects.all()
    t = Transaction.objects.all()
    
    ### slouží k filtrování transakcí
    myFilter = TransactionFilter(response.GET, queryset=t) 
    t = myFilter.qs

    ### počítá vložené typy produktů
    pt_count = pt.count()
    
    dict = {"pt": pt, "p": p, "s": s, "t": t,
            "myFilter": myFilter, "pt_count": pt_count}
    return render(response, "jp_app/list.html", dict)

### umožňuje vkládat všechny položky kategorie prodej
def create(response):
    # form = CreateProduct()
    # response.user
    form_pt = ProductTypeForm()
    form_p = ProductForm()
    form_s = SaleForm()
    form_t = TransactionForm()
    dict = {"form_pt": form_pt, "form_p": form_p, "form_s": form_s, "form_t": form_t}
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
        elif "save_s" in response.POST: ### prodejní kanál
            form_s = SaleForm(response.POST)
            if form_s.is_valid():
                # print(response.POST)
                form_s.save()
        elif "save_t" in response.POST: ### transakce
            form_t = TransactionForm(response.POST)
            # print(form_t.is_valid())
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
    dict = {"form_mt": form_mt, "form_m": form_m,
            "form_st": form_st, "form_r": form_r}
    if response.method == "POST":
        if "save_mt" in response.POST: ### typ skladové položky (materiálu)
            form_mt = MaterialTypeForm(response.POST)
            if form_mt.is_valid():
                form_mt.save()
        elif "save_m" in response.POST: ### materiál
            form_m = MaterialForm(response.POST)
            if form_m.is_valid():
                print(response.POST)
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
    
    # for item in form_st:
        
    #     print()        

    return render(response, "jp_app/material.html", dict)





###   NÁPADY   ###


### automaticky (pomocí ListView) načte seznam nápadů vložených pomocí "CreateIdea"
### jednodušší alternativa k řešení pomocí funkcí (viz výše)
class IdeaView(ListView):
    model = Idea
    template_name = 'jp_app/idea.html'
    ordering = ['-created'] ### seřadí seznam nápadů sestupně dle "data vložení"

    ### slouží k sečtení celkového počtu vložených položek "nápady" a následnému zobrazení na stránce
    def idea(self, response):
        i = Idea.objects.all()

        i_count = i.count()
        print(i_count)

        dict = {
           "i_count": i_count,
        }
        return render(response, "jp_app/idea.html", dict)
   
### zobrazí stránku s detailem dané položky "nápad" (url: "/idea/<id>", template: "idea.detail.html")
class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'jp_app/idea-detail.html'
    #template_name = 'idea-detail.html'

### automaticky (pomocí CreateView) načte formulář sloužící k vložení nápadů
class CreateIdea(CreateView):
    model = Idea ### models.py
    form_class = IdeaForm ### forms.py
    template_name = 'jp_app/idea_add.html' ### pokud kvůli bootstrap mám "template_name", musím zakomentovat "fields"
    # template_name = 'jp_app/idea_add.html'
    # fields = '__all__'


class UpdateIdea(UpdateView):
    model = Idea
    form_class = IdeaForm  ### forms.py
    template_name = 'jp_app/idea_update.html' ### pokud kvůli bootstrap mám "template_name", musím zakomentovat "fields"
    # fields = '__all__'


class DeleteIdea(DeleteView):
    model = Idea
    template_name = 'jp_app/idea_delete.html'
    success_url = reverse_lazy('jp_app:idea') ### 'reverse_lazy' slouží k určení stránky, na kterou po smazání nápadu bude přesměrováno


