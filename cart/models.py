from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from pos.models import BaseModelWithUUID
from account.models import Account

from item.models import Item

# Create your models here.

class Cart(BaseModelWithUUID):


    account = models.ForeignKey(to=Account, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account.username} Cart'

class CartItem(BaseModelWithUUID):

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    cart = models.ForeignKey(to=Cart,null=False,blank=False, on_delete=models.CASCADE)
    item = models.ForeignKey(to=Item, verbose_name="Cart Item Reference", null=True, blank=False, default=None, on_delete=models.SET_NULL)
    quantity = models.IntegerField(verbose_name="Cart Item Quantity", blank=True, null=False, default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.cart.account.username} - {self.item.name}'