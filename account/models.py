from django.db import models
from django.contrib.auth.models import Group, AbstractUser, User

# Create your models here.

class Account(AbstractUser):
    class Meta:
            verbose_name = 'Account'
            verbose_name_plural = 'Accounts'
