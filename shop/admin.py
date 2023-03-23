from django.contrib import admin

from .models import Shop, ShopCategory

# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    pass

admin.site.register(Shop, ShopAdmin)

class ShopCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(ShopCategory, ShopCategoryAdmin)