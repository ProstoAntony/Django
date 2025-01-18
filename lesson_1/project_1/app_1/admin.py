from django.contrib import admin
from .models import Mebel

class MebelAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'pars_datetime', 'description']
    list_display_links = ['id', 'pars_datetime']
    search_fields = ['id', 'price', 'pars_datetime', 'description']
    list_editable = [ 'price']
    list_filter = ['price', 'pars_datetime']


admin.site.register(Mebel, MebelAdmin)





