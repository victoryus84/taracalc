from django.contrib import admin
from django.utils.html import format_html
from .models import *


def custom_col_name(field_name, new_name):
    def column_name(obj):
        value = getattr(obj, field_name)
        if isinstance(value, bool):
            if value:
                return format_html('<img src="{0}" alt="Yes">', "/static/app/icons/Alpha_Green/green-check.ico") 
            else:
                return format_html('<img src="{0}" alt="No">', "/static/app/icons/Alpha_Red/red-blank.ico")
        elif hasattr(obj, f'get_{field_name}_display'):
            return getattr(obj, f'get_{field_name}_display')()
        return value
    column_name.short_description = new_name
    return column_name    

# Register your models here.
class DocumentItemInline(admin.TabularInline):
    model = DocumentItem
    fields = (
        'position',
        'nomenclature',
        'taratype',
        'quantity',
        'price',
        'total',
    )
    readonly_fields = (
        'position',
    )
    ordering = ['-document', 'position']       
    
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ( 'type', 'is_active',)}),
        ('Данные', {"fields": ( 'date', 'contragent', 'transport')}),
        ('Данные НН', {"fields": ( 'is_factura', 'number')}),
        ('Итоги', {"fields": ( 'total_per_document',)}),
    )
    exclude = ('is_deleted', 'deleted_by')
    inlines = (
        DocumentItemInline,
    )    
    list_display = (
        custom_col_name('date', 'Дата'),
        custom_col_name('is_active', 'Проведен'),
        custom_col_name('type', 'Вид'),  
        custom_col_name('is_factura', 'НН'),       
        custom_col_name('number', 'Номер НН'), 
        custom_col_name('contragent', 'Контрагент'),      
        custom_col_name('transport', 'Транспорт'),     
        custom_col_name('total_per_document', 'Всего') 
    )
    list_filter = (
        'type', 
        'contragent', 
        'date'
    )
    search_fields = (
        'contragent',
    )
    ordering  = ['-date']

    # class Media:
    #     js = [
    #         '/static/app/js/menu_filter_collapse.js',
    #     ] 
   