from djongo import models


class LivroModel(models.Model):
    titulo = models.CharField("Título", max_length=200)
    editora = models.CharField("editora", max_length=200)
    nome = models.CharField(null=True, max_length=100)
    categoria = models.CharField(null=True, max_length=50)
    quantidade = models.IntegerField(null=True)
    validade = models.DateField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.titulo
