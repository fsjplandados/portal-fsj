from django.contrib import admin
from .models import Categoria, Dashboard, LogAcesso

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cor_hex')

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'data_atualizacao', 'admin_only', 'is_new')
    list_filter = ('categoria', 'admin_only')
    search_fields = ('titulo', 'descricao')

@admin.register(LogAcesso)
class LogAcessoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'dashboard_titulo', 'data_acesso')
    list_filter = ('usuario', 'data_acesso')
    readonly_fields = ('usuario', 'dashboard_titulo', 'data_acesso') # Ninguém pode alterar o log
    search_fields = ('usuario__username', 'dashboard_titulo')
