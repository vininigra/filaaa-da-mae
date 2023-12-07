from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError


from .forms import RequerenteForm, ProdutoForm

# Create your tests here.


class cadastroProdutoTest(TestCase):
    # Testa se a página de cadastro de produtos retorna o código 200
    def test_cadastro_produto(self):
        response = self.client.get("/cadastroProduto/")
        self.assertEqual(response.status_code, 200)

    # Testa o cadastro de um produto com valores inválidos, esperando a mensagem de erro
    def test_cadastro_produto_post_invalido(self):
        response = self.client.post(
            "/cadastroProduto/",
            {"nome": "teste", "validade": "01/01/2024", "quantidade": "-10"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quantidade não pode ser negativa")

    # Testa o cadastro de um produto com data de validade inválida, esperando a mensagem de erro
    def test_cadastro_produto_post_validade(self):
        response = self.client.post(
            "/cadastroProduto/",
            {"nome": "teste", "validade": "01/01/2020", "quantidade": "10"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Data de validade não pode ser anterior a data atual"
        )

    # Testa o cadastro de um produto com nome inválido, esperando a mensagem de erro
    def test_cadastro_produto_post_nome(self):
        response = self.client.post(
            "/cadastroProduto/",
            {"nome": "123", "validade": "01/01/2024", "quantidade": "10"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nome não pode ser numerico")


class requerenteCadastroTest(TestCase):
     # Testa se a página de cadastro de requerentes retorna o código 200
    def test_requerente_cadastro(self):
        response = self.client.get("/cadastroRequerente/")
        self.assertEqual(response.status_code, 200)

    # nome, email, telefone e alimento
    def test_requerente_cadastro_post(self):
        # Testa o cadastro de um requerente com valores válidos
        response = self.client.post(
            "/cadastroRequerente/",
            {
                "nome": "Thiago",
                "email": "thiago@hotmail.com",
                "telefone": "19998256345",
                "alimento": "Feijao",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_clean_nome_numeric(self):
         # Testa o formulário de requerente com nome numérico, esperando a mensagem de erro
        form_data = {
            "nome": "123",
            "email": "thiago@hotmail.com",
            "telefone": "123456789",
            "alimento": "Feijao",
        }
        form = RequerenteForm(data=form_data)

        # Verifica se o formulário não é válido
        self.assertFalse(form.is_valid())

        # Verifica se o erro esperado está presente no campo nome
        self.assertIn("nome", form.errors)
        self.assertEqual(form.errors["nome"][0], "Nome não pode ser numerico")

    # telefone deve conter 11 numeros

    def test_clean_telefone_invalid_length(self):
        # Testa o formulário de requerente com telefone inválido, esperando a mensagem de erro
        form_data = {
            "nome": "Thiago",
            "email": "thiago@hotmail.com",
            "telefone": "123456789",
            "alimento": "Feijao",
        }
        form = RequerenteForm(data=form_data)

        # Verifica se o formulário não é válido
        self.assertFalse(form.is_valid())

        # Verifica se o erro esperado está presente no campo telefone
        self.assertIn("telefone", form.errors)
        self.assertEqual(form.errors["telefone"][0], "Telefone deve conter 11 numeros")

    # email validacao
    def teste_clean_email_invalido(self):
        # Testa o formulário de requerente com e-mail inválido, esperando a mensagem de erro
        form_data = {"email": "thiago"}
        form = RequerenteForm(data=form_data)
        self.assertFalse(form.is_valid())
        errors_str = str(form.errors["email"])
        # self.assertIn("Email deve conter @", errors_str)


class IndexTest(TestCase):
    def setUp(self):
        # Configuração inicial para o teste da página de índice
        # self.resp = self.client.get(r("core:index"), follow=True)
        self.resp = self.client.get(reverse("index"))

    def test_status_code(self):
        # Testa se a página de índice retorna o código 200
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        # Testa se a página de índice utiliza o template correto
        self.assertTemplateUsed(self.resp, "index.html")

    def test_html(self):
        # Testa se a página de índice contém as tags HTML esperadas
        tags = (
            ("<html", 1),
            ("<head", 2),
            ("<title", 1),
            ("<body", 2),
            ("<br", 1),
            ("<button", 1),
            ("<div", 62),
            ("</div", 59),
            ("</button", 1),
            ("</body", 2),
            ("</html", 1),
            ("<h1", 1),
            ("</h1", 1),
            ("<h2", 83),
            ("</h2", 83),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
