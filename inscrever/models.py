from django.db import models


class Cuidador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    experiencia = models.TextField(blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    disponibilidade = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return self.nome
