from django.contrib import admin
from .models import Categoria, Dashboard

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cor_hex')

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'data_atualizacao', 'admin_only', 'is_new')
    list_filter = ('categoria', 'admin_only')
    search_fields = ('titulo', 'descricao')