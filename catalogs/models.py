from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
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

class Contragent(Catalogs):
     
    is_jur   = models.BooleanField(default=True)
    is_rez   = models.BooleanField(default=True)
    code_gov = models.CharField(max_length=13, blank=True, unique=True)    
    code_tva = models.CharField(max_length=9, blank=True, unique=True)

    def __str__(self):
        return "%s, %s, %s" % (self.id, self.name, self.code_gov)

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"
        ordering = ["id"]
        
class Nomenclature(Catalogs):
    
    price    = models.DecimalField(max_digits=12,  decimal_places=2)
   
    def __str__(self):
        return "%s, %s, %s" % (self.id, self.name, self.price)
    
    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатура"
        ordering = ["id"]
        
class Vehicles(Catalogs):
    
    driver = models.CharField(max_length=50)
    
    def __str__(self):
        return "%s, %s, %s" % (self.id, self.name, self.driver)
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ["id"]
