from django.db import models

from account.models import Account
from pos.models import BaseModelWithUUID

# Create your models here.
class ShopCategory(BaseModelWithUUID):

    name = models.CharField(verbose_name='Shop Category Name', max_length=120, null=False, blank=False)
    description = models.CharField(verbose_name='Shop Category Description', max_length=180, null=False, blank=False)


class Shop(BaseModelWithUUID):

    account = models.ForeignKey(to=Account, null=True, blank=False, on_delete=models.SET_NULL)
    name = models.CharField(verbose_name='Shop Name', max_length=120, null=False, blank=False)
    description = models.CharField(verbose_name='Shop Description', max_length=180, null=False, blank=False)
    categories = models.ManyToManyField(to=ShopCategory, blank=True)

    def __str__(self):
        return f'{self.name} - {self.account.username}'

