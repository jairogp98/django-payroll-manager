from tkinter import CASCADE
from django.db import models
from simple_history.models import HistoricalRecords
from apps.employees.models import Employee

class Attendance (models.Model):

    id = models.AutoField(primary_key = True)
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE, verbose_name = 'employee', null = False)
    date = models.DateField('date', null = False)
    entrance_time = models.DateTimeField('entrance_time', null = False)
    exit_time = models.DateTimeField('exit_time', null = True, default = None)
    hours_worked = models.FloatField('hours_worked', max_length= 255, null = True, default = None)

    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
