from django.db import models
from django.urls import reverse
import datetime
from datetime import date
from ckeditor.fields import RichTextField ### importuje textové pole s možností editace textu (velikost písma, barva atd.)

# Create your models here.

###   PRODEJ   ###


class ProductType(models.Model):  # typ produktu
    # název typu produktu (svíčka, vonný vosk, fifuzér apod.)
    name = models.CharField(max_length=256)
    # automaticky doplní čas přidání typu produktu
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"NÁZEV PRODUKTU: {self.name}, DRUH ZBOŽÍ: {self.type}"
        return f"{self.name}"


class Item(models.Model):  # položka (součást) produktu
    name = models.CharField(max_length=256)  # název položky
    # cena za danou součást prduktu (nikoliv za měrnou jednotku, ale za celý produkt
    costs = models.PositiveIntegerField()
    ### dodavatel dané součásti produktu (firma od které kupuji danou součást)
    supplier = models.CharField(max_length=256, default=None)
    ### odkaz na web výrobce/dodavatele dané součásti produktu
    link = models.URLField(blank=True, null=True, default=None)
    note = models.TextField(blank=True)  # poznámka
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, ({self.costs} Kč)"

class Product(models.Model): # prudukt (výrobek k prodeji)
    name = models.CharField(max_length=256)  # název produktu
    # typ produktu (svíčka / vonný vosk / difuzér atd.)
    product_type = models.ForeignKey(
        ProductType, related_name="product_types", on_delete=models.CASCADE) # volba tyupu produktu
    items = models.ManyToManyField(Item, related_name="productsit", blank=True, default=[]) ### součásti daného produktu
    production_costs = models.IntegerField(default=0)  # výrobní náklady, které se spočítají automaticky na základě položek "items"
    # prodaných ks / prodané množství (nezadává se při tvorbě produktu, ale automaticky při transakci)
    sold = models.IntegerField(default=0)
    ### uvádí postup/technologii výroby (např. recept); RichTextField umožní editaci textu (změna velikosti, barvy písma apod.)
    procedure = RichTextField(blank=True, null=True, default=None)
    # uvádí (a/n), zda se jedná o výrobek pod značkou J&P CANDLES nebo pod jinou značkou (externí spolupráce)
    jp_candles = models.BooleanField(default=True)
    note = models.TextField(blank=True)  # poznámka
    # automaticky doplní čas přidání produktu
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]
        managed = True
        db_table = 'product'

    def __str__(self):
        # return f"NÁZEV PRODUKTU: {self.name}, DRUH ZBOŽÍ: {self.type}"
        return f"{self.name}"
        # umožňuje proklik ze seznamu nápadů na detail daného nápadu
    
    # def save(self, *args, **kwargs):
    #     self.production_costs = self.productsit.costs.values_list()
    #     print(self.production_costs)
    #     return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # return reverse('idea-detail', args=(str(self.id)))
        return reverse('jp_app:product-detail', args=[self.id])
    
    
class SaleType(models.Model):  # typ prodejního kanálu
    # název typu prodejního kanálu (# trh / eshop / komisní prodej / kamenný obchod / externí spolupráce apod.)
    name = models.CharField(max_length=256)
    # automaticky doplní čas přidání typu kanálu
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Sale(models.Model):  # typ prodejního kanálu
    # např. název konkrétního trhu, název obchodu kde byla svíčka prodána, eshop atd.
    name = models.CharField(max_length=256)
    type = models.ForeignKey(
        SaleType, related_name="sale_types", on_delete=models.CASCADE)  # volba typu prodejního kanálu
    sold = models.TextField(default="")
    # uvádí (a/n), zda se jedná o prodejní kanál pod značkou JPcandles nebo pro výrobu pod jinou značkou (externí spolupráce)
    jp_candles = models.BooleanField()

    def __str__(self):
        # return f"PRODEJNÍ KANÁL: {self.name}, DRUH KANÁLU: {self.type}"
        return f"{self.name}"


class Transaction(models.Model):  # transakce
    day_of_sale = models.DateField(default=date.today)  # datum transakce
    # prodejní kanál
    sales_channel = models.ForeignKey(
        Sale, related_name="sales", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="products", on_delete=models.CASCADE)  # prodaný produkt
    # prodejní cena za 1 ks / produkt
    product_price = models.PositiveIntegerField()
    quantity_of_product = models.PositiveIntegerField()  # množství prodaného produktu
    total_price = models.IntegerField(blank=True)  # , default=0)
    # automaticky doplní čas přidání transakce
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["day_of_sale"]

    def __str__(self):
        return f"{self.product}"
    
    ### automaticky počítá celkovou utrženou částku dané transakce
    def save(self, *args, **kwargs):
        self.total_price = self.product_price * self.quantity_of_product
        return super().save(*args, **kwargs)
    
    # def total(self):
    #     #total = Transaction.objects.all().sum()
    #     return Transaction.objects.all().sum()



###   SKLAD   ###

class MaterialType(models.Model):  # typ skladového materiálu
    # název typu suroviny (vůně, sklenice atd.)
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"NÁZEV PRODUKTU: {self.name}, DRUH ZBOŽÍ: {self.type}"
        return f"{self.name}"


class Material(models.Model):  # skladový materiál
    name = models.CharField(max_length=256)  # název suroviny (vosk sójový XYZ apod.)
    type = models.ForeignKey(
        MaterialType, related_name="types", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    quantity_of_material = models.IntegerField(
        default=0, blank=True)  # množství materiálu
    price = models.IntegerField(default=0, blank=True)  # nákupní cena

    def __str__(self):
        # return f"NÁZEV PRODUKTU: {self.name}, DRUH ZBOŽÍ: {self.type}"
        return f"{self.name} (type: {self.type})"


class Storage(models.Model):  # naskladnění materiálu do skladu
    day_of_storage = models.DateField()  # datum naskladnění
    # prodejní kanál
    material_type = models.ForeignKey(
        MaterialType, related_name="material_types", on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material, related_name="materials", on_delete=models.CASCADE)  # přidaný materiál
    quantity_of_material = models.PositiveIntegerField()  # množství přidaného materiálu
    # celková cena (nikoliv za jednotku, ale celkem)
    price = models.IntegerField()
    shop = models.CharField(max_length=256, blank=True)
    url = models.URLField(blank=True)  # odkaz na produkt
    note = models.TextField(blank=True)  # poznámka
    # automaticky doplní čas přidání transakce
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.material}"


class Removal(models.Model):  # vyskladnění materiálu ze skladu
    day_of_removal = models.DateField()  # datum vyskladnění
    # prodejní kanál
    material_type = models.ForeignKey(
        MaterialType, related_name="removal_types", on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material, related_name="removals", on_delete=models.CASCADE)  # vyskladňovaný materiál
    # množství vyskladněného materiálu
    quantity_of_material = models.PositiveIntegerField()
    #price = models.IntegerField()  # celková cena (nikoliv za jednotku, ale celkem)
    #shop = models.CharField(max_length=256)
    #url = models.URLField()  # odkaz na produkt
    note = models.TextField(blank=True)  # poznámka
    # automaticky doplní čas přidání transakce
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created}"


class Counter(models.Model):
    pass


###   NÁPADY   ###


class Idea(models.Model):  # nápad na nový výrobek

    stutuses = (
        ("Čeká na zahájení", "Čeká na zahájení"),
        ("Připravuje se", "Připravuje se"),
        ("Nastal problém", "Nastal problém"),
        ("Hotovo", "Hotovo")
    )

    name = models.CharField(max_length=256)  # název výrobku
    product_type = models.ForeignKey(
        ProductType, related_name="product_types_2", on_delete=models.CASCADE)  # volba typu produktu
    production_costs = models.IntegerField()  # předpokládané výrobní náklady
    selling_price = models.IntegerField()  # předpokládaná prodejní cena
    introduction_day = models.DateField()  # datum uvedení na trh
    note = models.TextField(blank=True)  # poznámka
    status = models.CharField(
        max_length=256,
        choices=stutuses,
        default='Čeká na zahájení'
    )
    created = models.DateTimeField(auto_now_add=True) # automaticky doplní čas přidání transakce

    def __str__(self):
        return f"{self.name}"
    
    # umožňuje proklik ze seznamu nápadů na detail daného nápadu
    def get_absolute_url(self):
        # return reverse('idea-detail', args=(str(self.id)))
        return reverse('jp_app:idea-detail', args=[self.id])

    def idea(self):
        i = Idea.objects.all()
        i_count = i.count()
        print(i_count)
        return i_count
