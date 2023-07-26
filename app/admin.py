from django.contrib import admin
from .models import *
import datetime
from .utilities import send_activation_notification

# Register your models here.

# Custom AUTH block (start)

def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
            modeladmin.message_user(request, 'Письма с требованиями отправлены')
            send_activation_notifications.short_description = 'Отправка писем с требованиями активации'

class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
                    ('activated', 'Прошли'),
                    ('threedays', 'He прошли более 3 дней'),
                    ('week', 'He прошли более недели'),
                )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)

class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)
    
admin.site.register(AdvUser, AdvUserAdmin)

# Custom AUTH block (end)  

@admin.register(Contragent)
class ContragentAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'deleted_at', 'deleted_by')
    
@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'deleted_at', 'deleted_by')
    
@admin.register(Vehicles)
class VehiclesAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'deleted_at', 'deleted_by')
    
    
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
    
 