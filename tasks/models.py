from datetime import date

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError
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
    id = models.AutoField(primary_key=True, max_length=6)
    fechaInicio = models.DateField(null=False)
    fechaFin = models.DateField(null=False)
    nombre = models.CharField(max_length=20, null=False)

    def _str_(self):
        return self.nombre

    def fijarNombre(fecha1, fecha2):
        meses_espanol = {
            1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR', 5: 'MAY', 6: 'JUN',
            7: 'JUL', 8: 'AGO', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DIC'
        }

        # Extraer las partes necesarias de las fechas
        mes1 = meses_espanol[fecha1.month]
        anio1 = str(fecha1.year)[-2:]

        mes2 = meses_espanol[fecha2.month]
        anio2 = str(fecha2.year)[-2:]

        # Formatear el resultado
        resultado = f"{mes1}{anio1}-{mes2}{anio2}"
        return resultado


class Ciclo(models.Model):
    id = models.AutoField(primary_key = True, max_length=6)
    idPeriodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE, related_name='ciclos')#Permite acceder a todos los ciclos de un periodo dado mediante periodo.ciclos.all().
    numero = models.PositiveIntegerField(max_length=2, null=False)

    def __str__(self):
        texto = "Ciclo: {0} {1}"
        return texto.format(self.numero,self.idPeriodo.nombre)


class Sugerencia(models.Model):
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class EstadisticaPeriodo(models.Model):
    id = models.AutoField(primary_key = True)
    numMatriculados = models.PositiveIntegerField(max_length = 3, null = False)
    numAprobados = models.PositiveIntegerField(max_length = 3, null = False)
    numReprobados = models.PositiveIntegerField(max_length = 3, null = False)
    numDesertores = models.PositiveIntegerField(max_length = 3, null = False)
    numForaneos = models.PositiveIntegerField(max_length = 3, null = False)
    idPeriodo = models.OneToOneField(PeriodoAcademico, null = True, blank = True, on_delete=models.CASCADE)
    idCiclo = models.OneToOneField(Ciclo, null = True, blank = True, on_delete=models.CASCADE)
    idAdministrador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='estadisticas')

    def __str__(self):
        nombre_periodo = self.idPeriodo.nombre if self.idPeriodo and self.idPeriodo.nombre else ""
        nombre_ciclo = self.idCiclo.__str__() if self.idCiclo else ""
    
        texto = "Datos de {0} {1}"
        return texto.format(nombre_periodo, nombre_ciclo)

    #def validarUsuario(self):Validar que el usuario ingresado sea personal Administrativo
    def validarPeriodo_Ciclo(self):
        # Validar que sólo sea de PeriodoAcademico o Ciclo
        if self.idPeriodo and self.idCiclo:
            raise ValidationError('El grupo de estadísticas puede asociarse con Periodo Académico o Ciclo pero no con ambos')
        if not self.idPeriodo and not self.idCiclo:
            raise ValidationError('Debería asociarse el grupo de estadísticas con un Periodo Académico o Ciclo')

    def save(self, *args, **kwargs):
        # Validar antes de guardar
        self.validarPeriodo_Ciclo()
        super(EstadisticaPeriodo, self).save(*args, **kwargs)

class Perfil(models.Model):
    fechaNacimiento = models.DateField(default=date.today)
    fotoPerfil = models.ImageField(upload_to='fotos/%Y/%m/%d', blank=True, null=True)
    descripcion = models.TextField(blank=True, default='')
    usuarioInstagram = models.CharField(max_length=30, blank=True, default='')
    usuarioFacebook = models.CharField(max_length=30, blank=True, default='')
    usuarioTwitter = models.CharField(max_length=30, blank=True, default='')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

