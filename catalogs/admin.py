from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Contragent)
class ContragentAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'deleted_at', 'deleted_by')
    
@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'deleted_at', 'deleted_by')
    
@admin.register(Vehicles)
class VehiclesAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'deleted_at', 'deleted_by')