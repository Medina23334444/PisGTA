from django.db import models
class Cargos(models.TextChoices):
    SECRETARIA = 'SE', 'Secretaria'
    DECANO = 'DE', 'Decano'
    DIRECTOR_CARRERA = 'DC', 'Director de Carrera'
