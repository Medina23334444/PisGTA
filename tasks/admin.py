from django.contrib import admin
from .models import Rol, Usuario, RolPersona, PeriodoAcademico

admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(RolPersona)
admin.site.register(PeriodoAcademico)