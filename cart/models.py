from django.db import models

from pos.models import BaseModelWithUUID
from account.models import Account

# Create your models here.

class Cart(BaseModelWithUUID):

    account = models.ForeignKey(to=Account, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account.username} Cart'

class CartItem(BaseModelWithUUID):

    cart = models.ForeignKey(to=Cart,null=False,blank=False, on_delete=models.CASCADE)
    # item = models.ForeignKey(to=Item, verbose_name="Cart Item Reference", null=True, blank=False)
    quatity = models.IntegerField(verbose_name="Cart Item Quantity", blank=True, null=False, default=1)

    def __str__(self):
        return f'{self.cart.account.username}'