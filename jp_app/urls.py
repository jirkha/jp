from django.urls import path

from . import views
from .views import IdeaView, IdeaDetailView, CreateIdea, UpdateIdea, DeleteIdea

app_name = 'jp_app'

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("list", views.list, name="list"),
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("material/", views.material, name="material"),
    path("list_material/", views.list_material, name="list_material"),
    path("idea/", IdeaView.as_view(), name="idea"),
    path("idea/<int:pk>", IdeaDetailView.as_view(), name="idea-detail"),
    path("idea_update/<int:pk>", UpdateIdea.as_view(), name="idea_update"),
    path("idea_delete/<int:pk>", DeleteIdea.as_view(), name="idea_delete"),
    path("idea_add/", CreateIdea.as_view(), name="idea_add"),
    path("transaction_chart/", views.transaction_chart, name="transaction_chart"),
    # path('jp_candles/', include("jp_candles_app.urls"))
]