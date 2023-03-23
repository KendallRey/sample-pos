from django.contrib import admin
from .models import Account, AccountAddress

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id','email',)

admin.site.register(Account, AccountAdmin)

class AccountAddressAdmin(admin.ModelAdmin):
    list_display = ('id','name',)

admin.site.register(AccountAddress, AccountAddressAdmin)
