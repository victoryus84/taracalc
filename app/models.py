from django.db import models
# Change default auth 
# cvictor 05.06.2023
from django.contrib.auth.models import AbstractUser
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
