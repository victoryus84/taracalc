from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Contragent)
class ContragentAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'deleted_at', 'deleted_by')
    list_display = (
        'id', 
        'name', 
        'code_gov', 
    )
    list_filter = (
        'name', 
    )
    search_fields = (
        'name',
        '=code_gov', 
    )
    ordering  = ['id']
    
@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'deleted_at', 'deleted_by')
    list_display = (
        'id', 
        'name', 
        'price', 
    )
    list_filter = (
        'name', 
        'price', 
    )
    search_fields = (
        'name',
        '=price',
    )
    ordering  = ['id']
    
@admin.register(Vehicles)
class VehiclesAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'deleted_at', 'deleted_by')
    list_display = (
        'id', 
        'name', 
        'driver', 
    )
    list_filter = (
        'name',
        'driver' 
    )
    search_fields = (
        'name',
        'driver',
    )
    ordering  = ['id']