from django.db import models
from django.utils import timezone
from datetime import timedelta

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    # Valor padrão que você usava no dicionário CORES_CATEGORIA
    cor_hex = models.CharField(max_length=7, default="#64748b", help_text="Ex: #3b82f6")
    icone = models.CharField(max_length=20, default="📊", blank=True)

    def __str__(self):
        return self.nome

class Dashboard(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    link = models.URLField(verbose_name="URL do Painel")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    
    # Upload de imagem (substitui o base64 manual)
    imagem_capa = models.ImageField(upload_to='dashboard_covers/', blank=True, null=True)
    
    admin_only = models.BooleanField(default=False, verbose_name="Apenas Admin?")
    data_atualizacao = models.DateTimeField(default=timezone.now, verbose_name="Data dos Dados")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    # Lógica do Badge "NOVO" portada para o Django
    @property
    def is_new(self):
        return (timezone.now() - self.data_atualizacao) < timedelta(days=2)