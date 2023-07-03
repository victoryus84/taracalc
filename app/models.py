from django.db import models
from enum import Enum
from django.utils import timezone

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

class DocumentType(Enum):   # A subclass of Enum
    Income = "Приход"
    Outcome = "Расход"

class TaraType(Enum):   # A subclass of Enum
    Income = "Темное"
    Outcome = "Светлое"
        
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
    
    price    = models.DecimalField(max_digits=15,  decimal_places=2)
    
    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатура"

class Vehicles(Catalogs):
    
    driver = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
    
class Documents(models.Model):
    
    code       = models.CharField(max_length=14, blank=True, null=True, unique=True)
    type       = models.CharField(max_length=6, blank=False, choices=[(tag, tag.value) for tag in DocumentType])           
    
    created    = models.DateTimeField(editable=False, default=timezone.now)
    updated = models.DateTimeField(editable=False, default=timezone.now)
    
    is_deleted = models.BooleanField(default=False)
    deleted    = models.DateTimeField(editable=False, default=timezone.now)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        abstract = True
        ordering = ['created']

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
            self.updated = timezone.now()
        return super(settings.AUTH_USER_MODEL, self).save(*args, **kwargs)
    
    def soft_delete(self, user_id=None):
        self.is_deleted = True
        self.deleted_by = user_id
        self.deleted = timezone.now()
        self.save()

    def __str__(self):
        return self.name

class Document(Documents):
    
    is_factura = models.BooleanField(default=False)
    contragent = models.ForeignKey(Contragent, on_delete=models.DO_NOTHING, blank=False)     
    nomenclarture = models.ForeignKey(Nomenclature, on_delete=models.DO_NOTHING, blank=False)
    qty = models.IntegerField(default=1, blank=False, )
    date = models.DateField(auto_now=True) 
    nomenclarture_type = models.CharField(max_length=7, blank=False, choices=[(tag, tag.value) for tag in TaraType])  
    transport = models.ForeignKey(Vehicles, on_delete=models.DO_NOTHING, blank=True)
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
