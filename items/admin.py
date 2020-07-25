from django.contrib import admin
from .models import Item


@admin.register(Item)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost']
