from django.db import models
from apps.base.models import BaseModel
from simple_history.models import HistoricalRecords
from django.utils import timezone
from apps.companies.models import Company

class Employee (BaseModel):
    name = models.CharField('name', max_length = 255, blank = False, null =False)
    last_name = models.CharField('lastname', max_length = 255, blank = False, null =False)
    email = models.EmailField('mail', max_length = 255, unique = True)
    dob = models.DateField('date of birth', default = None, null = False)
    company = models.ForeignKey(Company, on_delete= models.CASCADE, verbose_name = 'company', default = None)
    salary_per_hour = models.FloatField('salary', max_length = 255, null = False, default = None)
    role = models.CharField('role', max_length = 255, null =True)

    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return (f"{self.name} {self.last_name}")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        
        return super(Employee, self).save(*args, **kwargs)        