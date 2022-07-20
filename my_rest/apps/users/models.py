from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords

class UserManager(BaseUserManager):

    def _create_user(self,email, name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            email = email,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_user(self,email, name, last_name, password = None, **extra_fields):
        return self._create_user(email, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self,email, name, last_name, password = None, **extra_fields):
        return self._create_user(email, name, last_name, password, True, True, **extra_fields)

class User (AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('mail', max_length = 255, unique = True)
    name = models.CharField('name', max_length = 255, blank = False, null =False)
    last_name = models.CharField('lastname', max_length = 255, blank = False, null =False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    def natural_key(self):
        return (self.email)

    def __str__(self):
        return self.email
