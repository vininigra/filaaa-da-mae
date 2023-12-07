from django import forms
from django.core.exceptions import ValidationError
from core.models import LivroModel


def validate_title(value):
    if len(value) < 10:
        raise ValidationError("Deve ter pelo menos dez caracteres")


class LivroForm(forms.ModelForm):
    class Meta:
        model = LivroModel
        fields = ["nome", "categoria", "quantidade", "validade"]
        error_messages = {
            "nome": {
                "required": ("Informe o nome a ser cadastrado."),
            },
            "quantidade": {
                "required": ("Informe a quantidade"),
            },
            "validade": {
                "required": ("Informe a validade"),
            },
        }

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"]
        validate_title(titulo)
        return titulo

    def clean_editora(self):
        editora = self.cleaned_data["editora"]
        validate_title(editora)
        return editora

    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        validate_title(nome)
        return nome

    # def clean_categoria(self):
    #     categoria = self.cleaned_data["categoria"]
    #     validate_title(categoria)
    #     return categoria

    def clean_quantidade(self):
        quantidade = self.cleaned_data["quantidade"]
        validate_title(quantidade)
        return quantidade

    def clean_vencimento(self):
        vencimento = self.cleaned_data["vencimento"]
        validate_title(vencimento)
        return vencimento

    def clean(self):
        self.cleaned_data = super().clean()
        return self.cleaned_data
