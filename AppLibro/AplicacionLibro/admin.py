from django.contrib import admin
from .models import LibroDiario, EntradaDiario

class LibroDiarioAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LibroDiario._meta.fields]

class EntradaDiarioAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EntradaDiario._meta.fields]

admin.site.register(LibroDiario, LibroDiarioAdmin)
admin.site.register(EntradaDiario, EntradaDiarioAdmin)
