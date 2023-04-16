from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator

from pos.models import BaseModelWithUUID
from shop.models import Shop
from pos.directories import ITEM_IMAGES_DIR
# Create your models here.

class ItemCategory(BaseModelWithUUID):

    class Meta :
        verbose_name = 'Item Category'
        verbose_name_plural = 'Item Categories'

    shop = models.ForeignKey(to=Shop, null=True, blank=False, on_delete=models.SET_NULL)
    name = models.CharField(max_length=180, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f'{self.shop.name} - {self.name}'

class Item(BaseModelWithUUID):

    shop = models.ForeignKey(to=Shop, null=True, blank=False, on_delete=models.SET_NULL)
    name = models.CharField(max_length=180, null=False, blank=False)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=0)
    categories = models.ManyToManyField(to=ItemCategory, blank=True, related_name="categories")
    stock = models.IntegerField(null=False, blank=False, default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    image = models.ImageField(upload_to=ITEM_IMAGES_DIR, blank=True, null=True,)

    def __str__(self):
        shop_name = ""
        
        if self.shop is not None:
            shop_name = shop_name.join(f' - {self.shop.name}')
        return f'{self.name}{shop_name}'
