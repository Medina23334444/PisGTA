from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from .choices import Cargos

class Usuario(models.Model):
    dni = models.CharField(max_length=11, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, unique=True)


    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Rol(models.Model):
    nombre = models.CharField(max_length=20)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Cuenta(models.Model):
    clave = models.CharField(max_length=128)
    correo = models.EmailField(max_length=254, unique=True)
    estado = models.BooleanField(default=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='cuentas')
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.correo

    def set_password(self, raw_password):
        self.clave = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.clave)


