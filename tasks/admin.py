from django.contrib import admin
from .models import Rol, Usuario, RolPersona, PeriodoAcademico, EstadisticaPeriodo

admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(RolPersona)
admin.site.register(PeriodoAcademico)
admin.site.register(EstadisticaPeriodo)