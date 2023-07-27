from django.db import models
from django.utils import timezone
from django.db.models import Max, Sum
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
# Change default auth 
# cvictor 05.06.2023
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from users.models import User
# 05.06.2023

# Create your models here.

# Custom AUTH block (start)
class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True,verbose_name='Слать оповещение о новых комментариях?')
    
    class Meta(AbstractUser.Meta):
        pass
# Custom AUTH block (end)  
      
class Catalogs(models.Model):
    
    name     = models.CharField(max_length=150, blank=False) 
    name_full= models.CharField(max_length=600, blank=True)  
    
    created    = models.DateTimeField(editable=False, default=timezone.now)
    updated = models.DateTimeField(editable=False, default=timezone.now)
    
    is_deleted = models.BooleanField(default=False)
    deleted    = models.DateTimeField(editable=False, default=timezone.now)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        abstract = True
        ordering = ['name']
        
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
            self.updated = timezone.now()
        return super().save(*args, **kwargs)

    def soft_delete(self, user_id=None):
        self.is_deleted = True
        self.deleted_by = user_id
        self.deleted = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class Contragent(Catalogs):
     
    is_jur   = models.BooleanField(default=True)
    is_rez   = models.BooleanField(default=True)
    code_gov = models.CharField(max_length=13, blank=True, unique=True)    
    code_tva = models.CharField(max_length=9, blank=True, unique=True)

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"

class Nomenclature(Catalogs):
    
    price    = models.DecimalField(max_digits=12,  decimal_places=2)
    
    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатура"

class Vehicles(Catalogs):
    
    driver = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
    
class Documents(models.Model):
    
    TYPE_CHOICES = [
        ('0',"Приход"), 
        ('1',"Расход"),
        ('2',"Перемещение"),
        ('3',"Возврат"),
    ] 
    code       = models.CharField(max_length=14, blank=True, null=True, unique=True)
    type       = models.CharField(max_length=1, blank=False, choices=TYPE_CHOICES, default='1')           
    
    created    = models.DateTimeField(editable=False, default=timezone.now)
    updated = models.DateTimeField(editable=False, default=timezone.now)
    
    is_deleted = models.BooleanField(default=False)
    deleted    = models.DateTimeField(editable=False, default=timezone.now)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        abstract = True
        ordering = ['created']

    def soft_delete(self, user_id=None):
        self.is_deleted = True
        self.deleted_by = user_id
        self.deleted = timezone.now()
        self.save()

    def __str__(self):
        return self.type

class Document(Documents):
    
    is_factura = models.BooleanField(
        default=False
        )
    
    contragent = models.ForeignKey(
        Contragent, 
        on_delete=models.DO_NOTHING, 
        blank=False
        )
         
    date = models.DateField(
        auto_now=True
        ) 
    
    transport = models.ForeignKey(
        Vehicles, 
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True
        )
    
    total_per_document = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        )
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['-created']
        
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
            self.updated = timezone.now()
        return super(Document, self).save(*args, **kwargs)
        
class DocumentItem(models.Model):
    
    TARA_CHOICES = [
        ('0',"Светлое"), 
        ('1',"Темное"),
        ('2',"Белое"),
    ] 
    document = models.ForeignKey(
        Document,
        models.CASCADE,
        related_name='items',
    )
    position = models.PositiveIntegerField(
        verbose_name=_('Position'),
        editable=False,
        db_index=True,
    )
    nomenclature = models.ForeignKey(
        Nomenclature,
        models.PROTECT,
    )
    taratype = models.CharField(
        max_length=1, 
        blank=False, 
        choices=TARA_CHOICES, 
        default='0'  
    )    
    price = models.DecimalField(
        _('Price'),
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=10,
        decimal_places=3,
        default=0,
    )
    total = models.DecimalField(
        _('Total'),
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    
    class Meta:
        verbose_name = "Товар в документе"
        verbose_name_plural = "Товары в документах"
        ordering = ['-document', 'position']
        
    def save(self, *args, **kwargs):
        if not self.position:
            position = self.document.items.aggregate(Max('position'))['position__max'] or 0
            self.position = position + 1
        self.price = self.nomenclature.price 
        self.total = self.price * self.quantity
        
        super(DocumentItem, self).save(*args, **kwargs)
        
@receiver(pre_save, sender=DocumentItem)
def update_total(sender, instance, **kwargs):
    instance.total = instance.price * instance.quantity        
    print('Updated total')    
        
        
