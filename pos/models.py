import uuid
import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

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

class RequestStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    ACCEPTED = 'ACCEPTED', _('Accepted')
    REJECTED = 'REJECTED', _('Rejected')