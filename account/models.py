from django.db import models
from django.contrib.auth.models import Group, AbstractUser
from pos.models import BaseModelWithUUID
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Account(BaseModelWithUUID):

    user = models.OneToOneField(to=AbstractUser,null=True, blank=True, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50, verbose_name='First Name')
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Middle Name')
    last_name = models.CharField(max_length=50, verbose_name='Last Name')

    def __str__(self):
        return f'{self.last_name}, {self.first_name} {self.middle_name}'
