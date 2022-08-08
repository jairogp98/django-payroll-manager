from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords
from apps.companies.models import Company

class UserManager(BaseUserManager):

    def _create_user(self,email, name, last_name, password, is_staff, is_superuser, company, **extra_fields):
        user = self.model(
            email = email,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            company = company,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_user(self,email, name, last_name, company, password = None,  **extra_fields):
        return self._create_user(email, name, last_name, password, False, False, company, **extra_fields)

    def create_superuser(self,email, name, last_name, company, password = None,  **extra_fields):
        return self._create_user(email, name, last_name, password, True, True,company, **extra_fields)

class User (AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('mail', max_length = 255, unique = True)
    name = models.CharField('name', max_length = 255, blank = False, null =False)
    last_name = models.CharField('lastname', max_length = 255, blank = False, null =False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    company = models.ForeignKey(Company, on_delete= models.CASCADE, verbose_name = 'company', default = None, null = True)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name', 'company']

    def natural_key(self):
        return (self.email)

    def __str__(self):
        return self.email
