
from django.contrib import admin
from django.urls import path, include
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('admiManage/', views.admiManage, name='admiManage'),
    path('iniciarSesion/', views.iniciarSesion, name='iniciarSesion'),
    path('editarPersonalAdmi/<str:id>/', views.editarPersonalAdmi, name='editarPersonalAdmi'),
    path('registrarUsuario/', views.registrarUsuario, name='registrarUsuario'),
    path('eliminarUsuario/<id>', views.eliminarUsuario, name='eliminarUsuario'),
    path('homeAdministrador/', views.homeAdministrador, name='homeAdministrador'),
    path('perfilAdministrador/', views.perfilAdministrador, name='perfilAdministrador'),
    path('homePersonal/', views.homePersonal, name='homePersonal'),
    path('mostrarPeriodos/', views.mostrarPeriodos, name='mostrarPeriodos'),
    path('gestionPeriodos/', views.guardar_editar_Periodos, name='gestionPeriodos'),
    path('obtener_eventos/', views.obtener_eventos),
    path('registrarPeriodo/', views.registrarPeriodo),
    path('cerrar_sesion', views.cerrarSesion, name='cerrar_sesion'),
    path('Prediccion/', views.graficaPrediccion, name='GraficaPrediccion'),
    path('api/', include('tasks.urls')),
    path('datosHistoricos/', views.datosHistoricos, name='datosHistoricos'),
    path('sugerencia/', views.sugerenciaPersonal, name='sugerenciaPersonal'),
    path('modeloMatematico/', views.modeloMatematico, name='modeloMatematico'),
    path('agregarDatos/', views.variablesAdministrador, name='agregarDatos'),
]