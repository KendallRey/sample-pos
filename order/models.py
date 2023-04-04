from django.db import models
from django.db.models import F
from django.utils.timezone import now
from pos.models import BaseModelWithUUID
from account.models import Account, AccountAddress
from item.models import Item
from cart.models import CartItem
from shop.models import Shop

# Create your models here.

class OrderItem(BaseModelWithUUID):

    account = models.ForeignKey(to=Account, null=False, blank=False, on_delete=models.CASCADE)
    address = models.ForeignKey(to=AccountAddress, null=False, blank=False, on_delete=models.CASCADE)
    # item = models.ForeignKey(to=Item, null=True, blank=False, default=None, on_delete=models.SET_NULL)
    cart_item = models.ForeignKey(to=CartItem, null=True, blank=False, on_delete=models.SET_NULL)
    shop = models.ForeignKey(to=Shop, null=True, blank=False, editable=False, on_delete=models.SET_NULL)

    quantity = models.IntegerField(verbose_name="Order Item Quantity", null=False, blank=True, default=1)
    status = models.CharField(max_length=40, verbose_name="Order Item Status")
    date_placed = models.DateTimeField(verbose_name="Date Order Placed", editable=False, default=now)
    date_out = models.DateField(verbose_name="Date Order Out for Delivery", null=True, blank=True, default=None)
    date_received = models.DateField(verbose_name="Date Order Received", null=True, blank=True, default=None)
    date_cancelled = models.DateField(verbose_name="Date Order Cancelled", null=True, blank=True, default=None)
    is_cancelled = models.BooleanField(verbose_name="Date Order is Cancelled", blank=True, default=False)

    def __str__(self):
        return f'{self.account.username}-{self.cart_item.item.name}'
    
    def save(self, keep_deleted=False, **kwargs):
        # Item.objects.filter(id=self.cart_item.item.id).update(stock = F('stock')+(-self.cart_item.quantity))
        self.shop = self.cart_item.item.shop
        return super(OrderItem, self).save(keep_deleted, **kwargs)