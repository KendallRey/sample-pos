from django.db import models
from django.contrib.auth.models import Group, AbstractUser, User

from pos.models import BaseModelWithUUID

from pos.directories import user_directory_path

# Create your models here.

class Account(AbstractUser):

    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True,)

    class Meta:
            verbose_name = 'Account'
            verbose_name_plural = 'Accounts'

class AccountAddress(BaseModelWithUUID):
    class Meta :
        verbose_name = 'Account Address'
        verbose_name_plural = 'Account Addresses'

    account = models.ForeignKey(to=Account, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, verbose_name="Account Name", null=False)
    address = models.CharField(max_length=160, verbose_name="Account Address", null=False)
    latitude = models.CharField(max_length=160, verbose_name="Latitude", null=True, blank=True)
    longitude = models.CharField(max_length=160, verbose_name="Longitude", null=True, blank=True)

    def __str__(self):
         return f'{self.account.username}-{self.name}'