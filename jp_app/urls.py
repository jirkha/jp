from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("list", views.list, name="list"),
    path("", views.home, name="home"),
    path("create/", views.create, name="create")
    # path('jp_candles/', include("jp_candles_app.urls"))
]
