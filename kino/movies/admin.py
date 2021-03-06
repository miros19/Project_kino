from django.contrib import admin


from .models import *

#Customizing display models for movies and tickets
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'rating')
    search_fields = ('title', 'price', 'rating')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
class TicketAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'movie_id')
    search_fields = ('account_id', 'movie_id')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

#Registering models with custom views
admin.site.register(Movie, MovieAdmin)
admin.site.register(Ticket, TicketAdmin)