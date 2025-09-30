from django.contrib import admin
from .models import Category,Post,Heading


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ("name","title","parent","slug")
    search_fields = ("name","title","parent","slug")
    list_filter = ("parent",)
    ordering = ("name",)
