from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    search_fields = ('email', 'name')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)
