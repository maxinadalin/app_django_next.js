from django.urls import path
from .views import GetCategories, GetPost

urlpatterns = [
    path("categorias",GetCategories.as_view()),
    path("post/<id>",GetPost.as_view()),
]
