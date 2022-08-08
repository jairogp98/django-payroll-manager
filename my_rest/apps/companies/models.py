from django.db import models
from apps.base.models import BaseModel
from simple_history.models import HistoricalRecords
from django.utils import timezone

class Company (BaseModel):
    name = models.CharField('name', max_length = 255, blank = False, null =False)
    category = models.CharField('category', default= None,max_length = 255, null =True)
    email = models.EmailField('mail', max_length = 255, unique = True)
    phone = models.CharField('phone',max_length = 255, null = False)

    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return (self.name)
