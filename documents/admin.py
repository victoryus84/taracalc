from django.contrib import admin
from .models import *
# Register your models here.
class DocumentItemInline(admin.TabularInline):
    model = DocumentItem
    fields = (
        'position',
        'nomenclature',
        'taratype',
        'price',
        'quantity',
        'total',
    )
    readonly_fields = (
        'position',
    )
    ordering = ['position']       
    
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'deleted_by')
    inlines = (
        DocumentItemInline,
    )    
    list_display = (
        'type', 
        'code', 
        'date', 
        'is_factura', 
        'contragent', 
        'transport',
        'total_per_document',
    )
    list_filter = (
        'type', 
        'contragent', 
        'date'
    )
    search_fields = (
        '=number',
    )
    ordering  = ['-date']
    
 