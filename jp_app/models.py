from django.db import models
from django.urls import reverse

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


class Product(models.Model): # prudukt (výrobek k prodeji)
    name = models.CharField(max_length=256)  # název produktu
    # typ produktu (svíčka / vonný vosk / difuzér atd.)
    product_type = models.ForeignKey(
        ProductType, related_name="product_types", on_delete=models.RESTRICT) # volba tyupu produktu
    production_costs = models.IntegerField()  # výrobní náklady
    selling_price = models.IntegerField()  # prodejní cena
    # automaticky doplní čas přidání produktu
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        # return f"NÁZEV PRODUKTU: {self.name}, DRUH ZBOŽÍ: {self.type}"
        return f"{self.name})"


class Sale(models.Model):  # typ prodejního kanálu
    # např. názen trhu, název obchodu kde byla svíčka prodána, eshop atd.
    name = models.CharField(max_length=256)
    # trh / eshop / komisní prodej / externí spolupráce
    type = models.CharField(max_length=128)
    # uvádí (a/n), zda se jedná o prodejní kanál pod značkou JPcandles nebo pro výrobu pod jinou značkou (externí spolupráce)
    jp_candles = models.BooleanField()

    def __str__(self):
        # return f"PRODEJNÍ KANÁL: {self.name}, DRUH KANÁLU: {self.type}"
        return f"{self.name}"


class Transaction(models.Model):  # transakce
    day_of_sale = models.DateField()  # datum transakce
    # prodejní kanál
    sales_channel = models.ForeignKey(
        Sale, related_name="sales", on_delete=models.RESTRICT)
    product = models.ForeignKey(
        Product, related_name="products", on_delete=models.RESTRICT)  # prodaný produkt
    quantity_of_product = models.IntegerField()  # množství prodaného produktu
    # automaticky doplní čas přidání transakce
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product}"




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
        MaterialType, related_name="types", on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True)
    quantity_of_material = models.IntegerField(default=0, blank=True) # množství materiálu
    price = models.IntegerField(default=0, blank=True) # nákupní cena

    def __str__(self):
        # return f"NÁZEV PRODUKTU: {self.name}, DRUH ZBOŽÍ: {self.type}"
        return f"{self.name} (type: {self.type})"


class Storage(models.Model):  # naskladnění materiálu do skladu
    day_of_storage = models.DateField()  # datum naskladnění
    # prodejní kanál
    material_type = models.ForeignKey(
        MaterialType, related_name="material_types", on_delete=models.RESTRICT)
    material = models.ForeignKey(
        Material, related_name="materials", on_delete=models.RESTRICT)  # přidaný materiál
    quantity_of_material = models.IntegerField()  # množství přidaného materiálu
    price = models.IntegerField() # celková cena (nikoliv za jednotku, ale celkem)
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
        MaterialType, related_name="removal_types", on_delete=models.RESTRICT)
    material = models.ForeignKey(
        Material, related_name="removals", on_delete=models.RESTRICT)  # vyskladňovaný materiál
    quantity_of_material = models.IntegerField()  # množství vyskladněného materiálu
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
    product_type = models.ForeignKey(ProductType, related_name = "product_types_2", on_delete = models.RESTRICT)  # volba typu produktu
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
