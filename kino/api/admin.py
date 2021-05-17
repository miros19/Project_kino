from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

#Customizing your model display
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    search_fields = ('email', 'name')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

#Registering model with custom view
admin.site.register(Account, AccountAdmin)
#Unregister unnecessery model
admin.site.unregister(Group)
