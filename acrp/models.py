import time

from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
from django.urls import reverse
from requests import Response
from rest_framework.decorators import api_view


class Centro(models.Model):
    nombre = models.CharField(max_length=75)
    logo = models.ImageField(upload_to='centros/', null=True)
    direccion = models.CharField(max_length=150)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

def query_Centros_actives():
    queryset = Centro.objects.filter(activo__exact = True)
    return {
        'items': queryset,
    }

class Boletin(models.Model):
    titulo = models.CharField(max_length=75)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=5000)
    pdf = models.FileField(max_length=1000, blank=True, upload_to='boletines/')

    def __str__(self):
        return self.titulo

class Mensaje(models.Model):
    nombreRemitente = models.CharField(max_length=75)
    correoRemitente = models.EmailField(max_length=75)
    telefonoRemitente = models.CharField(max_length=15)
    fecha = models.DateField()
    mensaje = models.CharField(max_length=1000)

    def __str__(self):
        return self.fecha.__str__()

class Publicacion(models.Model):
    titulo = models.CharField(max_length=75)
    categoria = models.CharField(max_length=150)
    fecha = models.DateField(null=True)
    descripcion = models.CharField(max_length=5000)
    pdf = models.FileField(max_length=1000, blank=True, upload_to='publicaciones/')

    def __str__(self):
        return self.titulo


class Miembro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='miembro')
    centro = models.ForeignKey(Centro, blank=True, on_delete=models.SET_DEFAULT, default=0)
    categoria = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150)
    resumenCV = models.CharField(max_length=500,  default='cantidad de cosas que sabe hacer')
    activo = models.BooleanField()
    foto = models.ImageField(upload_to='members/', null=True)
    boletines = models.ManyToManyField(Boletin, related_name='autores', blank=True)
    publicaciones = models.ManyToManyField(Publicacion, related_name='autores', blank=True)
    mensajes = models.ManyToManyField(Mensaje, related_name='miembros', blank=True)

    def __str__(self):
        return self.usuario.first_name + ' ' + self.usuario.last_name

class Proyecto(models.Model):
    titulo = models.CharField(max_length=75)
    categoria = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=5000)
    pdf = models.FileField(max_length=1000, blank=True)
    miembros = models.ManyToManyField(Miembro, related_name='proyectos', blank=True)

    def __str__(self):
        return self.titulo


class Noticia(models.Model):
    titulo = models.CharField(max_length=75)
    categoria = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=5000)
    imagen = models.ImageField(upload_to='noticias/', null=True)

    def __str__(self):
        return self.titulo


class Evento(models.Model):
    nombre = models.CharField(max_length=75)
    centro = models.ForeignKey(Centro, blank=True, on_delete=models.SET_DEFAULT, default=0)
    categoria = models.CharField(max_length=150)
    direccion = models.CharField(max_length=175)
    descripcion = models.CharField(max_length=5000)
    fecha = models.DateField()

    def __str__(self):
        return self.nombre

