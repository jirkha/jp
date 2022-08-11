from django.db import models
import datetime
from datetime import date
# importuje textové pole s možností editace textu (velikost písma, barva atd.)
from ckeditor.fields import RichTextField

# Create your models here.

class ToDoList(models.Model):
    name = models.CharField(max_length=256)  ### název úkolu
    content = RichTextField(blank=True, null=True)  ### poznámka
    checked = models.BooleanField()
    date = models.DateField(blank=True, null=True)  # termín úkolu
    created = models.DateTimeField(auto_now_add=True) ### automaticky doplní čas přidání úkolu
