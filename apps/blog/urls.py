from django.urls import path
from .views import GetCategories

urlpatterns = [
    path("categorias",GetCategories.as_view())
]
