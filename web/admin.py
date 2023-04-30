from django.contrib import admin

# Register your models here.
from .models import Categoria, Producuto

admin.site.register(Categoria)
#admin.site.register(Producuto)

@admin.register(Producuto)
class ProducutoAdmin(admin.ModelAdmin):
    list_display = ('nombre','precio','Categoria')
    list_editable = ('precio',)