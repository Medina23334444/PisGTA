from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import Cargos


class Usuario(AbstractUser):
    dni = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, unique=True)

    def str(self):
        return f"{self.nombres} {self.apellidos}"


class Rol(models.Model):
    nombre = models.CharField(max_length=20)
    estado = models.BooleanField(default=True)
    user = models.ManyToManyField(Usuario, related_name='usuarios', through='RolPersona')

    def str(self):
        return self.nombre


class RolPersona(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} {self.rol}"


class Sugerencia(models.Model):
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
