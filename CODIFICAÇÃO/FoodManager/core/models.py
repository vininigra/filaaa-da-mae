from django.db import models

# Create your models here.
from mongoengine import Document, fields


class Produto(Document):
    # Campo para armazenar o nome do produto com no máximo 100 caracteres
    nome = fields.StringField(max_length=100)
    # Campo para armazenar a quantidade do produto como um número inteiro
    quantidade = fields.IntField()
    # Campo para armazenar a data e hora de validade do produto
    validade = fields.DateTimeField()
