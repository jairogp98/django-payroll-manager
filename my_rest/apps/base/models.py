from django.db import models

class BaseModel(models.Model):
        """Base model parent for every future model"""

        id = models.AutoField(primary_key = True)
        created_date = models.DateField('creation date', default = None, null = True)
        modified_date = models.DateField('modification date', default = None, null = True)
        deleted_date = models.DateField('delete date', default = None, null = True)

        class Meta:

            abstract = True
            verbose_name = "Base model"
            verbose_name_plural = "Base models"