import uuid
import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
import base64, uuid
from django.core.files.base import ContentFile
from rest_framework import serializers

class BaseModelWithUUID(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        raise NotImplementedError(f"__str__() should be defined for {self.__class__.__name__}")

    def hard_delete(self):
        return super(SafeDeleteModel,self).delete()

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,') # format ~= data:image/X,
            ext = format.split('/')[-1] # guess file extension
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name = id.urn[9:] + '.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)

class RequestStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    ACCEPTED = 'ACCEPTED', _('Accepted')
    REJECTED = 'REJECTED', _('Rejected')

class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    ACCEPTED = 'ACCEPTED', _('Accepted')
    CANCELLED = 'CANCELLED', _('Cancelled')
    PREPARING = 'PREPARING', _('Preparing')
    SHIPPING = 'SHIPPING', _('Shipping')
    OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', _('Out for Delivery')
    DELIVERED = 'DELIVERED', _('Delivered')
    RECEIVED = 'RECEIVED', _('Received')