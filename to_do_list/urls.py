from django.urls import path

from . import views
#from .views import IdeaView

app_name = 'to_do_list'


urlpatterns = [
    path("to_do_list/", views.to_do_list, name="to_do_list"),
    path("to_to_list-update/<int:id>",
         views.to_to_list_update, name="to_to_list_update"),
]
