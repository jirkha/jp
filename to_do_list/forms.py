from django import forms
from .models import ToDoList
from django.forms import ModelForm
# importuje textové pole s možností editace textu (velikost písma, barva atd.)
from ckeditor.fields import RichTextField

import datetime
from datetime import date


class DateInput(forms.DateInput):
    input_type = 'date'
    
    
class ToDoListForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ["name", "content", "checked", "date"]
        labels = {
            'name': ('Úkol'),
            'content': ('Obsah'),
            'checked': ('Hotovo'),
            'date': ('Datum vložení'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Název položky', 'title': 'Your name'}),
            'content': RichTextField(),
            #'checked': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'date': DateInput()}
