from django.contrib import admin

from .models import OrderItem
# Register your models here.

class OrderItemAdmin(admin.ModelAdmin):
    pass

admin.register(OrderItem, OrderItemAdmin)
