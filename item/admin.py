from django.contrib import admin

from .models import Item, ItemCategory

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)

class ItemCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(ItemCategory, ItemCategoryAdmin)