from django.contrib import admin
from .models import Cuidador

@admin.register(Cuidador)
class CuidadorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'cidade', 'estado', 'disponibilidade']
    search_fields = ['nome', 'email', 'cidade']
    list_filter = ['estado', 'disponibilidade']
