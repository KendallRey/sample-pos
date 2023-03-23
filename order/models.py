from django.db import models
from django.utils.timezone import now

from pos.models import BaseModelWithUUID
from account.models import Account, AccountAddress

# Create your models here.

class OrderItem(BaseModelWithUUID):

    account = models.ForeignKey(to=Account, null=False, blank=False, on_delete=models.CASCADE)
    address = models.ForeignKey(to=AccountAddress, null=False, blank=False, on_delete=models.CASCADE)
    # item = models.ForeignKey(to=Item, null=True, blank=False, default=None, on_delete=models.SET_NULL)

    quantity = models.IntegerField(verbose_name="Order Item Quantity", null=False, blank=True, default=1)
    status = models.CharField(max_length=40, verbose_name="Order Item Status")
    date_placed = models.DateTimeField(verbose_name="Date Order Placed", editable=False, default=now)
    date_out = models.DateField(verbose_name="Date Order Out for Delivery", null=True, blank=True, default=None)
    date_received = models.DateField(verbose_name="Date Order Received", null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.account.username}-'