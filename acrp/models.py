import time

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from requests import Response
from rest_framework.decorators import api_view


class Centro(models.Model):
    nombre = models.CharField(max_length=75)
    logo = models.ImageField(upload_to='centros/', null=True)
    direccion = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre


class Miembro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='miembro')
    centro = models.ForeignKey(Centro, blank=True, on_delete=models.DO_NOTHING)
    categoria = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150)
    resumenCV = models.CharField(max_length=500,  default='cantidad de cosas que sabe hacer')
    activo = models.BooleanField()
    foto = models.ImageField(upload_to='members/', null=True)

    def __str__(self):
        return self.usuario.first_name + ' ' + self.usuario.last_name


class Proyecto(models.Model):
    titulo = models.CharField(max_length=75)
    categoria = models.CharField(max_length=150)
    pdf = models.FileField(max_length=1000, blank=True)
    miembros = models.ManyToManyField(Miembro, related_name='proyectos', blank=True)

    def __str__(self):
        return self.titulo


class Publicacion(models.Model):
    titulo = models.CharField(max_length=75)
    categoria = models.CharField(max_length=150)
    pdf = models.FileField(max_length=1000, blank=True)
    autores = models.ManyToManyField(Miembro, related_name='publicaciones', blank=True)

    def __str__(self):
        return self.titulo


class Evento(models.Model):
    nombre = models.CharField(max_length=75)
    centro = models.ForeignKey(Centro, blank=True, on_delete=models.DO_NOTHING)
    categoria = models.CharField(max_length=150)
    direccion = models.CharField(max_length=175)
    fecha = models.DateField()

    def __str__(self):
        return self.nombre
