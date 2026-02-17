from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
# 👇 1. IMPORTANTE: Adicionei o LogAcesso aqui na importação
from .models import Dashboard, Categoria, LogAcesso 

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

    categorias = Categoria.objects.all()

    # 👇 2. O BLOCO QUE FALTAVA (O "Dedo-Duro")
    # Isso salva no banco toda vez que a tela carrega
    try:
        # Define um texto descritivo para o log
        descricao_log = "Acessou a Home Geral"
        
        if busca_query:
            descricao_log = f"Buscou por: '{busca_query}'"
        elif categoria_id:
            descricao_log = f"Filtrou Categoria ID: {categoria_id}"

        # Salva efetivamente no banco
        LogAcesso.objects.create(
            usuario=request.user,
            dashboard_titulo=descricao_log # Usamos esse campo para descrever a ação
        )
    except Exception as e:
        # Se der erro no log, não trava o site pro usuário, apenas avisa no console
        print(f"Erro ao gerar log: {e}")
    # ---------------------------------------------------------

    context = {
        'dashboards': dashboards,
        'categorias': categorias,
        'busca_atual': busca_query,
        'cat_atual': int(categoria_id) if categoria_id else None,
        'eh_diretoria': eh_diretoria
    }
    
    return render(request, 'dashboards/index.html', context)
