### imports

from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import ToDoList

from .forms import ToDoListForm


### views

def to_do_list(response):
    t = ToDoList.objects.all()
    
    if response.method == "POST":
        print("POST")
        if "add" in response.POST:
            name = response.POST.get('name')
            print("name: ", name)
            date = response.POST.get('date')
            print("date: ", date)
            content = response.POST.get('content')
            checked = response.POST.get('checked')
            print("checked: ", checked)
            if checked == "on":
                checked = True
            else:
                checked = False
            print("checked: ", checked)
            new_t = ToDoList(
                name=name,
                date=date,
                #date=None,
                content=content,
                #checked=True,
                checked=checked,
                )
            new_t.save()
        
        elif "delete_t" in response.POST:
            ### uloží "id" položky, kterou chceme smazat
            x = response.POST['delete_t']
            ### vyhledá odpovídající položku (dle id=x)
            z = ToDoList.objects.get(id=x)
            z.delete()  # vymaže danou položku
            messages.success(response, ('Úkol byl úspěšně vymazán'))
    
    dict = {
        "t": t,
    }
    return render(response, "to_do_list/to_do_list.html", dict)


def to_to_list_update(response, id):
    item = ToDoList.objects.get(id=id)
    form = ToDoListForm(response.POST or None,
                    instance=item)
    if form.is_valid():
        form.save()
        messages.success(response, ('Úkol byl úspěšně změněn'))
        return redirect("/to_do_list")

    dict = {
        "form": form,
        "item": item,
    }

    return render(response, "to_do_list/to_to_list-update.html", dict)
