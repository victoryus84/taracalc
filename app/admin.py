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
    
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_factura', 'code', 'type', 'date', 'contragent', 'nomenclarture', 'nomenclarture_type', 'transport']
    list_filter = ['type', 'contragent', 'date']
    exclude = ('is_deleted', 'deleted_at', 'deleted_by')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj is None:  # Check if creating a new instance
            form.base_fields['code'].disabled = True

        return form

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        form = super().formfield_for_choice_field(db_field, request, **kwargs)

        if db_field.name == 'is_factura':
            selected_value = request.POST.get('is_factura')

            if selected_value == 'True':
                form.base_fields['code'].disabled = False

        return form