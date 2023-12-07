from django.urls import path
from .views import cadastroRequerente

from . import views

urlpatterns = [
    # Página inicial que renderiza a pesquisa na coleção "Produtos"
    path("", views.index, name="index"),
    # Página de cadastro de produtos
    path("cadastroProduto/", views.cadastroProduto, name="cadastroProduto"),
    # Página de cadastro de requerentes
    path("cadastroRequerente/", views.cadastroRequerente, name="cadastroRequerente"),
    # Página para listar produtos
    path("listarProdutos/", views.listarProdutos, name="listarProdutos"),
    # Página para listar requerentes
    path("listarRequerente/", views.listarRequerentes, name="listarRequerente"),
    # Página para listar contas
    path("listarConta/", views.listarConta, name="listarConta"),
    # Página de cadastro de doações
    path("cadastroDoacao/", views.cadastroDoacao, name="cadastroDoacao"),
    # Página para remover um alimento com base no ID do alimento
    path(
        "remover_alimento/<str:alimento_id>/",
        views.remover_alimento,
        name="remover_alimento",
    ),
    # path("index_with_total/", views.index_with_total, name="index_with_total"),
]
