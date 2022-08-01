from django.urls import path

from . import views
from .views import IdeaView, IdeaDetailView, CreateIdea, UpdateIdea, DeleteIdea
from .views import ProductView, ProductDetailView, CreateProduct, UpdateProduct, DeleteProduct


app_name = 'jp_app'

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:id>", views.index, name="index"),
    
    path("list", views.list, name="list"),
    path("create/", views.create, name="create"),
    
    path("product/", ProductView.as_view(), name="product"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product-detail"),
    path("product_update/<int:pk>", UpdateProduct.as_view(), name="product_update"),
    path("product_delete/<int:pk>", DeleteProduct.as_view(), name="product_delete"),
    path("product_add/", CreateProduct.as_view(), name="product_add"),
    
    path("item/", views.item, name="item"),
    path("item_update/<int:id>", views.item_update, name="item_update"),

    path("material/", views.material, name="material"),
    path("list_material/", views.list_material, name="list_material"),
    
    path("material_chart/", views.material_chart, name="material_chart"),
    path("statistic/", views.statistic, name="statistic"),
    path("stat_chart/", views.stat_chart, name="stat_chart"),
    
    path("google/", views.google, name="google"),
    
    path("idea/", IdeaView.as_view(), name="idea"),
    path("idea/<int:pk>", IdeaDetailView.as_view(), name="idea-detail"),
    path("idea_update/<int:pk>", UpdateIdea.as_view(), name="idea_update"),
    path("idea_delete/<int:pk>", DeleteIdea.as_view(), name="idea_delete"),
    path("idea_add/", CreateIdea.as_view(), name="idea_add"),
    
    # path('jp_candles/', include("jp_candles_app.urls"))
]