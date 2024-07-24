
from django.contrib import admin
from django.urls import path, include
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('manage-user/', views.manage_user, name='manage_user'),
    path('admiManage/', views.admiManage, name='admiManage'),
    path('iniciarSesion/', views.iniciarSesion, name='iniciarSesion'),
    path('editarPersonalAdmi/<str:id>/', views.editarPersonalAdmi, name='editarPersonalAdmi'),
    path('registrarUsuario/', views.registrarUsuario, name='registrarUsuario'),
    path('eliminarUsuario/<id>', views.eliminarUsuario, name='eliminarUsuario'),
    path('homeAdministrador/', views.homeAdministrador, name='homeAdministrador'),
    path('perfilAdministrador/', views.perfilAdministrador, name='perfilAdministrador'),
    path('homePersonal/', views.homePersonal, name='homePersonal'),
    #URLs Periodo Academico
    path('mostrarPeriodos/',views.mostrarPeriodos, name='mostrarPeriodos'),
    #path('mostrarRegistrarPeriodo/mostrarRegistrarPeriodo2/',views.guardar_editar_Periodos),
    path('gestionPeriodos/',views.guardar_editar_Periodos, name='gestionPeriodos'),
    path('obtener_eventos/', views.obtener_eventos),
    path('registrarPeriodo/',views.registrarPeriodo),
    path('cerrar_sesion', views.cerrarSesion, name='cerrar_sesion'),
    path('Prediccion/', views.graficaPrediccion, name='GraficaPrediccion'),
    path('api/', include('tasks.urls')),
    path('datosHistoricos/', views.datosHistoricos, name='datosHistoricos'),
    path('modeloMatematicoInfo/', views.modeloMatematicoInfo, name="modeloMatematicoInfo"),
    path('variableModelo/', views.variablesModelo, name="variablesModelo"),
    path('prediccionCiclos/', views.prediccionCiclos, name="prediccionCiclos"),
] 

