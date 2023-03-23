from django.db import models

from pos.models import BaseModelWithUUID
from shop.models import Shop
# Create your models here.

class ItemCategory(BaseModelWithUUID):

    shop = models.ForeignKey(to=Shop, null=True, blank=False, on_delete=models.SET_NULL)
    name = models.CharField(max_length=180, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f'{self.shop.name} - {self.name}'

class Item(BaseModelWithUUID):

    shop = models.ForeignKey(to=Shop, null=True, blank=False, on_delete=models.SET_NULL)
    name = models.CharField(max_length=180, null=False, blank=False)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=0)
    stock = models.IntegerField(null=False, blank=False, default=0) 

    def __str__(self):
        return f'{self.name} - {self.shop.name}'
