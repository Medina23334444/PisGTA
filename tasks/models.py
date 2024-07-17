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


class PeriodoAcademico(models.Model):
    id = models.AutoField(primary_key = True, max_length=6)
    fechaInicio = models.DateTimeField(null = False)
    fechaFin = models.DateTimeField(null = False)
    nombre = models.CharField(max_length = 20, null = False)
    #estado = models.BooleanField(null = False)

    def __str__(self):
        return self.nombre
    
    def fijarNombre(fecha1, fecha2):
        meses_espanol = {
            1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR', 5: 'MAY', 6: 'JUN',
            7: 'JUL', 8: 'AGO', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DIC'
        }
    
        # Extraer las partes necesarias de las fechas
        mes1 = meses_espanol[fecha1.month]
        año1 = str(fecha1.year)[-2:]
    
        mes2 = meses_espanol[fecha2.month]
        año2 = str(fecha2.year)[-2:]
    
        # Formatear el resultado
        resultado = f"{mes1}{año1}-{mes2}{año2}"
        return resultado
    
class Ciclo(models.Model):
    id = models.AutoField(primary_key = True, max_length=6)
    idPeriodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE, related_name='ciclos')#Permite acceder a todos los ciclos de un periodo dado mediante periodo.ciclos.all().
    numero = models.PositiveIntegerField(max_length = 2, null = False)

    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.numero,self.idPeriodo.nombre)

class Sugerencia(models.Model):
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
