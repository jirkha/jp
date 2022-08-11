### imports

from django.shortcuts import render

from .models import ToDoList


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
    
    dict = {
        "t": t,
    }
    return render(response, "to_do_list/to_do_list.html", dict)



