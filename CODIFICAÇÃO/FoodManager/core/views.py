from django.shortcuts import render, redirect
from django import forms
from bson import ObjectId
from django.http import HttpResponse
import unittest
from .forms import DoacaoForm, ProdutoForm, RequerenteForm
from .services.ConnectionService import ConnectionService
from .services.MongoServie import MongoService
from .services.repositories.FoodManagerRepository import FoodManagerRepository
from .services.CadastroProdutoService import (
    CadastroProdutoService,
    CadastroRequerenteService,
    DoacaoService,
)

# log

import logging
import unittest


# Create your views here.


def index(request):
    # renderizacao da pesquisa na collection produtos
    # Criar uma instância de ConnectionService para obter conexão com o MongoDB
    conexao = ConnectionService()
    # Criar uma instância de MongoService, especificando o banco de dados "FoodManager"
    mongo = MongoService(conexao, "FoodManager")
    # Criar uma instância de FoodManagerRepository, utilizando o MongoService para acesso ao banco de dados
    repository = FoodManagerRepository(mongo)
    # Obter todos os produtos da coleção "Produtos"
    produtos = list(repository.find("Produtos", **{}))
    # Renderizar a página "index.html" e passar a lista de produtos para o template
    return render(request, "index.html", {"produtos": produtos})


def cadastroProduto(request):
    # Verificar se a requisição é do tipo POST
    if request.method == "POST":
        # Criar uma instância do formulário ProdutoForm com os dados da requisição
        form = ProdutoForm(request.POST)        
        # Verificar se o formulário é válido
        if form.is_valid():
            # Criar instâncias de serviços e repositórios para interagir com o MongoDB
            conexao = ConnectionService()
            mongo = MongoService(conexao, "FoodManager")
            repository = FoodManagerRepository(mongo)
            # Criar uma instância do serviço CadastroProdutoService
            service = CadastroProdutoService(repository)
            # Inserir os dados do formulário na coleção "Produtos" usando o serviço
            service.insert(form.cleaned_data)
            # Redirecionar para a página de cadastro de produtos
            return redirect("cadastroProduto")
        else:
            # Se o formulário não for válido, renderizar a página com o formulário e mensagens de erro
            return render(request, "cadastroProduto.html", {"form": form})
    # Se a requisição não for do tipo POST, criar uma instância vazia do formulário ProdutoForm
    form = ProdutoForm()
    # Renderizar a página de cadastro de produtos com o formulário vazio
    return render(request, "cadastroProduto.html", {"form": form})


# cadastro de requerentes
def cadastroRequerente(request):
    produtos = []
    if request.method == "POST":
        form = RequerenteForm(request.POST)
        if form.is_valid():
            conexao = ConnectionService()
            mongo = MongoService(conexao, "FoodManager")
            repository = FoodManagerRepository(mongo)
            service = CadastroRequerenteService(repository)
            service.insert(form.cleaned_data)
            return redirect("cadastroRequerente")
        else:
            return render(
                request, "cadastroRequerente.html", {"form": form, "produtos": produtos}
            )
    form = RequerenteForm()
    return render(request, "cadastroRequerente.html", {"form": form})


def listarRequerentes(request):
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    requerentes = list(repository.find("Requerentes", **{}))
    return render(request, "listarRequerentes.html", {"requerentes": requerentes})


def listarConta(request):
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    conta = list(repository.find("Conta", **{}))
    return render(request, "listarConta.html", {"conta": conta})


# buscar ultimo registro no mongo
def buscarUltimoRegistro(request):
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    # repository = FoodManagerRepository(mongo)
    collection = mongo.db["Produtos"]
    print(collection)
    ultimoRegistro = collection.find_one({}, sort=[("_id", -1)])
    # logging.basicConfig(filename="log.txt", level=logging.INFO)
    logging.info(f"Ultimo Registro: {ultimoRegistro}")
    return render(request, "index.html", {"ultimoRegistro": ultimoRegistro})


def listarProdutos(request):
    # Conectar ao MongoDB
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)

    # Obter todos os produtos
    produtos = list(repository.find("Produtos", **{}))

    # Calcular a quantidade total
    quantidade_total = sum([produto["quantidade"] for produto in produtos])

    # Imprimir o conteúdo de produtos e a quantidade total para depuração
    print("Produtos:", produtos)
    print("Quantidade Total:", quantidade_total)

    # Passar os produtos e a quantidade total para o template
    return render(
        request,
        "listarProdutos.html",
        {"produtos": produtos, "quantidade_total": quantidade_total},
    )


# Minha colection de produtos
# _id 656f085fc0dd6e7dd306906c
# nome "Feijão"
# quantidade 5
# validade 2023-12-31T00:00:00.000+00:00
def cadastroDoacao(request):
    # Conectar ao MongoDB
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    print(conexao)
    # Obter todos os produtos
    produtos = list(repository.find("Produtos", **{}))

    # Filtrar produtos em estoque com quantidade acima de 1
    produtos_disponiveis = [
        produto for produto in produtos if produto["quantidade"] > 1
    ]

    # Obter a lista de nomes dos produtos disponíveis
    nomes_produtos_disponiveis = [produto["nome"] for produto in produtos_disponiveis]
    print(nomes_produtos_disponiveis)

    # Verificar se o formulário foi submetido
    if request.method == "POST":
        # Obter o nome do alimento selecionado no formulário
        alimento = request.POST.get("nomes_produtos_disponiveis")
        print(alimento)
        # Restante do código para processar o formulário...

    # Passar a lista de produtos disponíveis para o template
    return render(
        request,
        "cadastroRequerente.html",
        # "doacao.html",
        {
            "form": DoacaoForm(),
            "produtos_disponiveis": produtos_disponiveis,
            "nomes_produtos_disponiveis": nomes_produtos_disponiveis,
        },
    )


# remover alimento
def remover_alimento(request, alimento_id):
    # Conectar ao MongoDB
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    alimento_id = ObjectId(alimento_id)
    print(alimento_id)

    produto = repository.find("Produtos", filters={"_id": alimento_id})
    print(produto)
    if produto:
        repository.delete("Produtos", {"_id": alimento_id})
        repository.insert("Relatorio", **produto)
        return redirect("listarProdutos.html")
    else:
        return redirect("cadastroProduto.html")


# collection relatorio que ira receber os produtos que sairam da collection produtos e seram inseridos na collection relatorio com os dados do produto e dados do requerente


def relatorio(request):
    # Conectar ao MongoDB
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    # Obter todos os produtos
    produtos = list(repository.find("Produtos", **{}))
    # Obter todos os requerentes
    requerentes = list(repository.find("Requerentes", **{}))
    # Obter todos os requerentes
    print("Produtos:", produtos)
    # Passar os produtos e a quantidade total para o template
    return render(
        request,
        "relatorio",
        {
            "produtos": produtos,
            "requerentes": requerentes,
        },
    )


class TestMongoService(unittest.TestCase):
    def setUp(self):
        self.connection = ConnectionService()
        self.mongo_service = MongoService(self.connection, "test_db")
        self.repository = FoodManagerRepository(self.mongo_service)
