from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q # Importante para busca complexa (Título OU Descrição)
from .models import Dashboard, Categoria

@login_required
def home(request):
    busca_query = request.GET.get('q')
    categoria_id = request.GET.get('cat')
    
    # Lógica de Segurança (Quem vê o quê)
    eh_diretoria = request.user.is_superuser or request.user.groups.filter(name='Diretoria').exists()

    if eh_diretoria:
        dashboards = Dashboard.objects.all().order_by('-data_atualizacao')
    else:
        dashboards = Dashboard.objects.filter(admin_only=False).order_by('-data_atualizacao')

    # Filtros de Busca
    if busca_query:
        dashboards = dashboards.filter(
            Q(titulo__icontains=busca_query) | 
            Q(descricao__icontains=busca_query)
        )

    if categoria_id:
        dashboards = dashboards.filter(categoria_id=categoria_id)

    # 👇 A LINHA QUE ESTAVA FALTANDO É ESTA AQUI:
    categorias = Categoria.objects.all()

    context = {
        'dashboards': dashboards,
        'categorias': categorias, # Agora vai funcionar
        'busca_atual': busca_query,
        'cat_atual': int(categoria_id) if categoria_id else None,
        'eh_diretoria': eh_diretoria
    }
    
    return render(request, 'dashboards/index.html', context)