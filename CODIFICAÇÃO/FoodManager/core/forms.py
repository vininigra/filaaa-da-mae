from django import forms
from datetime import datetime

from .services.repositories.FoodManagerRepository import FoodManagerRepository
from .services.ConnectionService import ConnectionService
from .services.MongoServie import MongoService
from .services.CadastroProdutoService import CadastroRequerenteService

# produto, requerente, doador

# testes referentes a html e status

# Formulário para dados de produtos
class ProdutoForm(forms.Form):
    # Campo para o nome do produto com no máximo 100 caracteres
    nome = forms.CharField(max_length=100, required=True)
    # Campo para a quantidade do produto como um número inteiro
    quantidade = forms.IntegerField(required=True)
    # Campo para a data de validade do produto
    validade = forms.DateField(required=True)

    # Método de validação para o campo 'nome'
    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        if nome.isnumeric():
            raise forms.ValidationError("Nome não pode ser numerico")
        return nome
    # Método de validação para o campo 'quantidade'
    def clean_quantidade(self):
        quantidade = self.cleaned_data["quantidade"]
        if quantidade < 0:
            raise forms.ValidationError("Quantidade não pode ser negativa")
        return quantidade
    # Método de validação para o campo 'validade'
    def clean_validade(self):
        validade = self.cleaned_data["validade"]
        data_atual = datetime.now().date()
        if validade < data_atual:
            raise forms.ValidationError(
                "Data de validade não pode ser anterior a data atual"
            )
        return validade

# Formulário para dados de requerentes
class RequerenteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Inicializa o formulário, adicionando campos dinâmicos para escolher alimentos
        super().__init__(*args, **kwargs)
        # Cria uma instância do serviço de conexão ao MongoDB
        conexao = ConnectionService()
        # Cria uma instância do serviço MongoDB
        mongo = MongoService(conexao, "FoodManager")
        # Cria uma instância do repositório FoodManager
        food_manager = FoodManagerRepository(mongo)
        # Obtém a lista de alimentos da coleção "Produtos"
        alimentos = food_manager.find("Produtos", **{})
        # Cria uma lista de opções para o campo "alimento" no formato (id, nome)
        # opcoes = [(alimento['nome'], alimento['nome']) for alimento in alimentos]
        opcoes = [(str(alimento["_id"]), alimento["nome"]) for alimento in alimentos]
        # Adiciona um campo de escolha para os alimentos no formulário
        self.fields["alimento"] = forms.ChoiceField(choices=opcoes, required=True)
        # Adiciona um campo oculto para armazenar o ID do alimento selecionado
        self.fields["alimento_id"] = forms.CharField(
            widget=forms.HiddenInput(), required=True
        )

    nome = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=11, required=True)

    # Método de validação para o campo 'nome'
    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        # Verifica se o nome contém apenas caracteres não numéricos
        if nome.isnumeric():
            raise forms.ValidationError(
                "Nome não pode ser numerico", code="numeric_name"
            )
        return nome

    # Método de validação para o campo 'telefone'
    def clean_telefone(self):
        telefone = self.cleaned_data["telefone"]
        # Verifica se o telefone contém exatamente 11 números
        if len(telefone) != 11:
            raise forms.ValidationError("Telefone deve conter 11 numeros")
        return telefone

    # Método de validação para o campo 'email'
    def clean_email(self):
        email = self.cleaned_data["email"]
        # Verifica se o e-mail contém o caractere '@'
        if "@" not in email:
            raise forms.ValidationError("Email deve conter @")
        return email

    ## Método de validação para o campo 'alimento'
    def clean_alimento(self):
        alimento = self.cleaned_data["alimento"]
        # Verifica se o nome do alimento contém apenas caracteres não numéricos
        if alimento.isnumeric():
            raise forms.ValidationError(
                "Alimento não pode ser numerico", code="numeric_name"
            )
        return alimento


# class DoadorForm(forms.Form):
#     def clean_escolha_alimento(self):
#         escolha_alimento = self.cleaned_data["alimento"]
#         if escolha_alimento == "0":
#             raise forms.ValidationError("Escolha um alimento")
#         return escolha_alimento


class DoacaoForm(forms.Form):
    alimento = forms.ChoiceField(choices=[])


# # Minha colection de produtos
# # _id 656f085fc0dd6e7dd306906c
# # nome "Feijão"
# # quantidade 5
# # validade 2023-12-31T00:00:00.000+00:00
# # formulario para usuario poder selecionar o alimento que tem cadastrado e retirar
