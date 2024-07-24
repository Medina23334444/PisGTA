from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta

from .forms import UsuarioForm
from .models import Usuario, Rol, RolPersona, Sugerencia, PeriodoAcademico, Ciclo, Perfil, EstadisticaPeriodo
from django.contrib import messages
import tasks.RungeKutta as r
from django.http.response import JsonResponse
import json
from django.views.decorators.http import require_http_methods
import logging
logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'landingPage.html')


def iniciarSesion(request):
    if request.method == "POST":
        correo = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=correo, password=password)
            if user is not None:
                login(request, user)
                roles_persona = RolPersona.objects.filter(usuario=user)
                roles = [rp.rol for rp in roles_persona]
                if any(rol.nombre == 'Personal' for rol in roles):
                    return redirect('homePersonal')
                elif any(rol.nombre == 'Administrador' for rol in roles):
                    return redirect('homeAdministrador')
                else:
                    return redirect('homeDefault')
            else:
                if Usuario.objects.filter(username=correo).exists():
                    error = 'Contraseña incorrecta'
                else:
                    error = 'La cuenta no existe'
                messages.error(request, error)
                return render(request, 'iniciarSesion.html')

        except Exception as e:
            error = f'Error: {str(e)}'
            messages.error(request, error)
            return render(request, 'iniciarSesion.html')

    return render(request, 'iniciarSesion.html')


@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('home')


def registrarUsuario(request):
    if request.method == 'POST':
        data = request.POST
        dni = request.POST['dni']

        if not validar_cedula(dni):
            messages.error(request, 'La cédula ingresada no es válida.')
            return redirect('admiManage')


        try:
            with transaction.atomic():
                usuario = Usuario.objects.create(
                    username=request.POST['correo'],
                    email=request.POST['correo'],
                    dni=request.POST['dni'],
                    nombres=request.POST['nombres'],
                    apellidos=request.POST['apellidos'],
                    direccion=request.POST['direccion'],
                    telefono=request.POST['telefono'],
                )
                usuario.set_password(request.POST['dni'])
                usuario.save()

                if data['tipo_cargo'] == 'Administrador':
                    rol = Rol.objects.get(nombre='Administrador')
                elif data['tipo_cargo'] == 'Personal':
                    rol = Rol.objects.get(nombre='Personal')
                else:
                    messages.error(request, 'Tipo de cargo no válido.')
                    return redirect('admiManage')

                RolPersona.objects.create(rol=rol, usuario=usuario)

                messages.success(request, 'Usuario registrado correctamente!')
                return redirect('admiManage')

        except Rol.DoesNotExist:
            messages.error(request, 'El rol especificado no existe.')
            return redirect('admiManage')

        except IntegrityError:
            messages.error(request, 'Las credenciales ya han sido registradas por otro usuario.')
            return redirect('admiManage')

        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {e}')
            return redirect('admiManage')

    return render(request, 'admiManage.html')

def validar_cedula(cedula):
    if len(cedula) != 10:
        return False
    
    try:
        digitos_cedula = [int(d) for d in cedula]
    except ValueError:
        return False
    
    cod_provincia = int(cedula[:2])#Validar código de provincia
    if cod_provincia < 1 or cod_provincia > 24:
        return False
    
    digito_3 = digitos_cedula[2] #Validar digito 3, este entre 0 y 6
    if digito_3 < 0 or digito_3 > 6:
        return False
    
    #coefficients = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    
    for i in range(0,9):
        x = digitos_cedula[i]
        if i%2 == 0:
            x = x * 2
            if x > 9:
                x -= 9
        total += x
        """product = coefficients[i] * digitos_cedula[i]
        if product >= 10:
            product -= 9
        total += product"""
    
    digito_verificador = 10 - (total % 10)
    if digito_verificador == 10:
        digito_verificador = 0
    
    return digito_verificador == digitos_cedula[9]

@login_required
def editarPersonalAdmi(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario actualizado correctamente!')
            return redirect('admiManage')
        else:
            messages.error(request, 'Error al actualizar usuario. Por favor, revisa el formulario.')
        return redirect('admiManage')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'admiManage.html',
                  {'form': form, 'personalAdministrativo': Usuario.objects.all()})


@login_required
def eliminarUsuario(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return redirect('admiManage')


def admiManage(request):
    personalAdministrativo = Usuario.objects.all()
    return render(request, 'admiManage.html', {"personalAdministrativo": personalAdministrativo})


@login_required
def homeAdministrador(request):
    return render(request, 'homeAdministrador.html')


@login_required
def perfilAdministrador(request):
    usuario = request.user
    perfil = get_object_or_404(Perfil, usuario=usuario)
    return render(request, 'perfilAdministrador.html', {'usuario': usuario, 'perfil': perfil})


@login_required
def homePersonal(request):
    return render(request, 'homePersonal.html')


@login_required
def mostrarPeriodos(request):#Vista general de Periodos
    periodos = PeriodoAcademico.objects.all()
    #messages.success(request, '!Lista actualizada!')
    return render(request, "gestionPeriodoHome.html",{"periodos": periodos})


@login_required
def guardar_editar_Periodos(request):#Vista para editar o agregar
    periodos = PeriodoAcademico.objects.all()
    messages.success(request, '!Lista actualizada!')
    return render(request, "gestionPeriodo.html",{"periodos":periodos})


@login_required
def obtener_eventos(request):#Método para cargar los periodos registrados en calendar
    periodos = PeriodoAcademico.objects.all()
    eventos = []

    for periodo in periodos:
        eventos.append({
            'title': periodo.nombre,
            'start': periodo.fechaInicio.isoformat(),
            'end': (periodo.fechaFin + timedelta(days=1)).isoformat(),
            'allDay': True,
        })

    return JsonResponse(eventos, safe=False)


@login_required
def registrarPeriodo(request):
    # Se los recibe como strings
    fechaI_str = request.POST.get('fecha_inicio')
    fechaF_str = request.POST.get('fecha_fin')

    # Se los convierte
    fechaI = datetime.strptime(fechaI_str, '%Y-%m-%d').date()
    fechaF = datetime.strptime(fechaF_str, '%Y-%m-%d').date()
    nombreP = PeriodoAcademico.fijarNombre(fechaI, fechaF)

    # Condicional para guardar o editar
    try:  # Si puede convertir el id a entero, existe, debe actualizar
        idP = int(request.POST['txtId'])

        periodos_antiguos = PeriodoAcademico.objects.all().exclude(id=idP)
        if periodos_antiguos.exists():
            for periodo in periodos_antiguos:
                if periodo.fechaInicio <= fechaI <= periodo.fechaFin or periodo.fechaInicio <= fechaF <= periodo.fechaFin:
                    messages.error(request, '¡Las fechas coinciden con períodos anteriores. Revise!')
                    return redirect('/mostrarPeriodos/')

        periodo = PeriodoAcademico.objects.get(id=idP)
        periodo.fechaInicio = fechaI
        periodo.fechaFin = fechaF
        periodo.nombre = nombreP
        periodo.save()
    except ValueError:  # Si devuelve un ID nulo, crear

        periodos_antiguos = PeriodoAcademico.objects.all()
        if periodos_antiguos.exists():
            for periodo in periodos_antiguos:
                if periodo.fechaInicio <= fechaI <= periodo.fechaFin or periodo.fechaInicio <= fechaF <= periodo.fechaFin:
                    messages.error(request, '¡Las fechas coinciden con períodos anteriores. Revise!')
                    return redirect('/mostrarPeriodos/')

        periodo = PeriodoAcademico.objects.create(fechaInicio=fechaI, fechaFin=fechaF, nombre=nombreP)
        for i in range(1, 9):
            ciclo = Ciclo.objects.create(idPeriodo=periodo, numero=i)

    messages.success(request, '¡Período registrado correctamente!')
    return redirect('/mostrarPeriodos/')


def sugerenciaPersonal(request):
    if request.method == 'POST':
        try:
            sugerencia = Sugerencia.objects.create(
                asunto=request.POST['asunto'],
                descripcion=request.POST['descripcion'],
                usuario=request.user
            )
            messages.success(request, 'Sugerencia enviada con éxito.')
            return redirect('sugerenciaPersonal')
        except Exception as e:
            print(f'Ocurrió un error: {str(e)}')
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return redirect('sugerenciaPersonal')

    return render(request, 'sugerencia.html')



def graficaPrediccion(request):
    tiempo = r.lista_tiempo_prediccion()
    matriculados = r.lista_matriculados_prediccion()
    aprobados = r.lista_aprobados_prediccion()
    reprobados = r.lista_reprobados_prediccion()
    desertores = r.lista_desertores_prediccion()
    foraneos = r.lista_foraneos_prediccion()
    contexto = {'tiempo': tiempo, 'matriculados': matriculados, 'aprobados': aprobados, 'reprobados': reprobados, 'desertores': desertores, 'foraneos': foraneos}
    return render(request, 'InterfazPrediccion.html', contexto)


@login_required
def index(request):
    return render(request,'InterfazPrediccion.html')

@login_required
def index1(request):   
    return render(request,'InterfazCiclos.html')


@login_required
def variablesModelo(request):
    return render(request, 'variablesModelo.html')


def datosHistoricos(request):
    tiempo = r.lista_tiempo_prediccion()
    matriculados = r.lista_matriculados_prediccion()
    aprobados = r.lista_aprobados_prediccion()
    reprobados = r.lista_reprobados_prediccion()
    desertores = r.lista_desertores_prediccion()
    foraneos = r.lista_foraneos_prediccion()
    contexto = {'tiempo': tiempo, 'matriculados': matriculados, 'aprobados': aprobados, 'reprobados': reprobados, 'desertores': desertores, 'foraneos': foraneos}
    return render(request, 'datosHistoricos.html', contexto)

@login_required
def prediccionCiclos(request):
    return render(request, 'InterfazCiclos.html')


def generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF):
    chart = {
        'xAxis': [
            {
                'type': 'category',
                'data': listaT,
                'name': 'tiempo'
            }
        ],
        'yAxis': [
            {
                'type': "value",
                'name': 'Nro Estudiantes',
                'nameTextStyle': {
                    'left': '25%',
                    'padding': [0, 0, 0, -20], 
                    'fontSize': 12 
                }
            }
        ],
        'title': [
            {
                'text': 'Grafica Prediccion',
                'bottom': '92%'
            }
        ],
        'tooltip': [
            {
                'trigger': 'axis',
                'axisPointer': {
                    'type': 'cross',
                    'label': {
                        'backgroundColor': '#6a7985'
                    }
                }
            }
        ],
        'legend': [
            {
                'data': ['Foraneos', 'Desertores', 'Aprobados', 'Matriculados', 'Reprobados'],
                'bottom': '87%'
            }
        ],
        'toolbox': [
            {
                'feature': {
                    'saveAsImage': {}
                }
            }
        ],
        'dataZoom': [
            {
                'type': 'slider',
                'start': 0,
                'end': 100
            }
        ],
        'animationDuration': 2000,
        'animationEasing': 'cubicInOut',
        'series': [
            {
                'name': 'Foraneos',
                'type': "line",
                'smooth': True,
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': listaF
            },
            {
                'name': 'Desertores',
                'data': listaD,
                'type': "line",
                'smooth': True
            },
            {
                'name': 'Aprobados',
                'data': listaA,
                'type': "line",
                'smooth': True
            },
            {
                'name': 'Matriculados',
                'data': listaM,
                'type': "line",
                'smooth': True
            },
            {
                'name': 'Reprobados',
                'data': listaR,
                'type': "line",
                'smooth': True
            },
        ]
    }
    return chart

@require_http_methods(["GET", "POST"])
def get_chart(request):
    if request.method == "POST":
        logger.info("Recibida solicitud POST")
        data = json.loads(request.body)
        selected_year = int(data.get('year'))
        logger.info(f"Año seleccionado: {selected_year}")
        listaD = r.lista_desertores_prediccion()
        listaT = r.lista_tiempo_prediccion()
        listaA = r.lista_aprobados_prediccion()
        listaR = r.lista_reprobados_prediccion()
        listaM = r.lista_matriculados_prediccion()
        listaF = r.lista_foraneos_prediccion()
    else:
        logger.info("Recibida solicitud GET")
        listaD =[73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
        listaT = ['2023-04-29', '2020-07-24', '2022-07-02', '2022-08-28', '2021-06-15', '2022-01-03', '2022-04-17', '2022-10-02', '2022-12-31', '2022-05-25', '2021-08-24', '2021-05-14', '2020-01-28', '2022-03-08', '2022-10-05', '2020-04-19', '2023-08-19', '2023-11-08', '2021-02-26', '2020-03-02', '2021-10-22', '2023-03-11', '2023-10-16', '2022-07-01', '2023-10-06', '2020-10-27']
        listaA =[55, 71, 61, 64, 61, 87, 67, 56, 76, 55, 70, 47, 53, 70, 75, 69, 66, 64, 52, 60, 63, 79, 71, 49, 71, 63]
        listaR =[60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
        listaM =[60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
        listaF =[73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    chart = generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF)
    return JsonResponse(chart)

def get_chart1(request):
    listaD = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    listaT = ['2023-04-29', '2020-07-24', '2022-07-02', '2022-08-28', '2021-06-15', '2022-01-03', '2022-04-17', '2022-10-02', '2022-12-31', '2022-05-25', '2021-08-24', '2021-05-14', '2020-01-28', '2022-03-08', '2022-10-05', '2020-04-19', '2023-08-19', '2023-11-08', '2021-02-26', '2020-03-02', '2021-10-22', '2023-03-11', '2023-10-16', '2022-07-01', '2023-10-06', '2020-10-27']
    listaA = [55, 71, 61, 64, 61, 87, 67, 56, 76, 55, 70, 47, 53, 70, 75, 69, 66, 64, 52, 60, 63, 79, 71, 49, 71, 63]
    listaR = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaM = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaF = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    chart = generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF)
    return JsonResponse(chart)

def get_chart2(request):
    listaD = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    listaT = ['2023-04-29', '2020-07-24', '2022-07-02', '2022-08-28', '2021-06-15', '2022-01-03', '2022-04-17', '2022-10-02', '2022-12-31', '2022-05-25', '2021-08-24', '2021-05-14', '2020-01-28', '2022-03-08', '2022-10-05', '2020-04-19', '2023-08-19', '2023-11-08', '2021-02-26', '2020-03-02', '2021-10-22', '2023-03-11', '2023-10-16', '2022-07-01', '2023-10-06', '2020-10-27']
    listaA = [55, 71, 61, 64, 61, 87, 67, 56, 76, 55, 70, 47, 53, 70, 75, 69, 66, 64, 52, 60, 63, 79, 71, 49, 71, 63]
    listaR = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaM = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaF = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    chart = generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF)
    return JsonResponse(chart)

def get_chart3(request):
    listaD = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    listaT = ['2023-04-29', '2020-07-24', '2022-07-02', '2022-08-28', '2021-06-15', '2022-01-03', '2022-04-17', '2022-10-02', '2022-12-31', '2022-05-25', '2021-08-24', '2021-05-14', '2020-01-28', '2022-03-08', '2022-10-05', '2020-04-19', '2023-08-19', '2023-11-08', '2021-02-26', '2020-03-02', '2021-10-22', '2023-03-11', '2023-10-16', '2022-07-01', '2023-10-06', '2020-10-27']
    listaA = [55, 71, 61, 64, 61, 87, 67, 56, 76, 55, 70, 47, 53, 70, 75, 69, 66, 64, 52, 60, 63, 79, 71, 49, 71, 63]
    listaR = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaM = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaF = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    chart = generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF)
    return JsonResponse(chart)

def get_chart4(request):
    listaD = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    listaT = ['2023-04-29', '2020-07-24', '2022-07-02', '2022-08-28', '2021-06-15', '2022-01-03', '2022-04-17', '2022-10-02', '2022-12-31', '2022-05-25', '2021-08-24', '2021-05-14', '2020-01-28', '2022-03-08', '2022-10-05', '2020-04-19', '2023-08-19', '2023-11-08', '2021-02-26', '2020-03-02', '2021-10-22', '2023-03-11', '2023-10-16', '2022-07-01', '2023-10-06', '2020-10-27']
    listaA = [55, 71, 61, 64, 61, 87, 67, 56, 76, 55, 70, 47, 53, 70, 75, 69, 66, 64, 52, 60, 63, 79, 71, 49, 71, 63]
    listaR = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaM = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaF = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    chart = generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF)
    return JsonResponse(chart)

def get_chart5(request):
    listaD = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    listaT = ['2023-04-29', '2020-07-24', '2022-07-02', '2022-08-28', '2021-06-15', '2022-01-03', '2022-04-17', '2022-10-02', '2022-12-31', '2022-05-25', '2021-08-24', '2021-05-14', '2020-01-28', '2022-03-08', '2022-10-05', '2020-04-19', '2023-08-19', '2023-11-08', '2021-02-26', '2020-03-02', '2021-10-22', '2023-03-11', '2023-10-16', '2022-07-01', '2023-10-06', '2020-10-27']
    listaA = [55, 71, 61, 64, 61, 87, 67, 56, 76, 55, 70, 47, 53, 70, 75, 69, 66, 64, 52, 60, 63, 79, 71, 49, 71, 63]
    listaR = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaM = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaF = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    chart = generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF)
    return JsonResponse(chart)

def get_chart6(request):
    listaD = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    listaT = ['2023-04-29', '2020-07-24', '2022-07-02', '2022-08-28', '2021-06-15', '2022-01-03', '2022-04-17', '2022-10-02', '2022-12-31', '2022-05-25', '2021-08-24', '2021-05-14', '2020-01-28', '2022-03-08', '2022-10-05', '2020-04-19', '2023-08-19', '2023-11-08', '2021-02-26', '2020-03-02', '2021-10-22', '2023-03-11', '2023-10-16', '2022-07-01', '2023-10-06', '2020-10-27']
    listaA = [55, 71, 61, 64, 61, 87, 67, 56, 76, 55, 70, 47, 53, 70, 75, 69, 66, 64, 52, 60, 63, 79, 71, 49, 71, 63]
    listaR = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaM = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaF = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    chart = generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF)
    return JsonResponse(chart)

def get_chart7(request):
    listaD = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    listaT = ['2023-04-29', '2020-07-24', '2022-07-02', '2022-08-28', '2021-06-15', '2022-01-03', '2022-04-17', '2022-10-02', '2022-12-31', '2022-05-25', '2021-08-24', '2021-05-14', '2020-01-28', '2022-03-08', '2022-10-05', '2020-04-19', '2023-08-19', '2023-11-08', '2021-02-26', '2020-03-02', '2021-10-22', '2023-03-11', '2023-10-16', '2022-07-01', '2023-10-06', '2020-10-27']
    listaA = [55, 71, 61, 64, 61, 87, 67, 56, 76, 55, 70, 47, 53, 70, 75, 69, 66, 64, 52, 60, 63, 79, 71, 49, 71, 63]
    listaR = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaM = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaF = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    chart = generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF)
    return JsonResponse(chart)

def get_chart8(request):
    listaD = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    listaT = ['2023-04-29', '2020-07-24', '2022-07-02', '2022-08-28', '2021-06-15', '2022-01-03', '2022-04-17', '2022-10-02', '2022-12-31', '2022-05-25', '2021-08-24', '2021-05-14', '2020-01-28', '2022-03-08', '2022-10-05', '2020-04-19', '2023-08-19', '2023-11-08', '2021-02-26', '2020-03-02', '2021-10-22', '2023-03-11', '2023-10-16', '2022-07-01', '2023-10-06', '2020-10-27']
    listaA = [55, 71, 61, 64, 61, 87, 67, 56, 76, 55, 70, 47, 53, 70, 75, 69, 66, 64, 52, 60, 63, 79, 71, 49, 71, 63]
    listaR = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaM = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaF = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    chart = generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF)
    return JsonResponse(chart)

def get_chart9(request):
    listaD = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    listaT = ['2023-04-29', '2020-07-24', '2022-07-02', '2022-08-28', '2021-06-15', '2022-01-03', '2022-04-17', '2022-10-02', '2022-12-31', '2022-05-25', '2021-08-24', '2021-05-14', '2020-01-28', '2022-03-08', '2022-10-05', '2020-04-19', '2023-08-19', '2023-11-08', '2021-02-26', '2020-03-02', '2021-10-22', '2023-03-11', '2023-10-16', '2022-07-01', '2023-10-06', '2020-10-27']
    listaA = [55, 71, 61, 64, 61, 87, 67, 56, 76, 55, 70, 47, 53, 70, 75, 69, 66, 64, 52, 60, 63, 79, 71, 49, 71, 63]
    listaR = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaM = [60, 74, 78, 77, 59, 64, 71, 78, 62, 65, 56, 55, 76, 82, 67, 78, 71, 61, 71, 84, 67, 84, 40, 76, 68, 64]
    listaF = [73, 66, 74, 84, 65, 65, 84, 76, 62, 73, 63, 63, 70, 47, 49, 61, 57, 71, 58, 52, 83, 65, 68, 52, 62, 69]
    chart = generate_chart_data(listaT, listaD, listaA, listaR, listaM, listaF)
    return JsonResponse(chart)



@login_required
def modeloMatematico(request):
    return render(request, 'modeloMatematicoInfo.html')


@login_required
def variablesAdministrador(request):
    return render(request, 'agregarDatos.html')


def listaSugerencias(request):
    sugerencias = Sugerencia.objects.all()
    return render(request, 'listaSugerencia.html', {"sugerencias": sugerencias})


def mostrarDatosHistoricos(request):
    periodos = PeriodoAcademico.objects.all()

    # Arreglo para almacenar los periodos con sus estadísticas
    datos = []

    for periodo in periodos:
        estadisticas_ciclo = EstadisticaPeriodo.objects.filter(idCiclo__idPeriodo=periodo)# Estadísticas asociadas con ciclos específicos

        # Estadística total del periodo, sin asociación con ciclos
        estadistica_general = EstadisticaPeriodo.objects.filter(idPeriodo=periodo, idCiclo=None).first()

        datos.append({
            'periodo': periodo,
            'estadisticas_ciclo': estadisticas_ciclo,
            'estadistica_general': estadistica_general
        })

    context = {
        'datos': datos
    }

    return render(request, "mostrarDatosHistoricos.html", context)


def mostrarDatosPeriodo(request, id):
    estadisticasPeriodo = EstadisticaPeriodo.objects.filter(idCiclo__idPeriodo = id)
    #IDEA: Mostrar todos los periodos en tabla y mostrar error en los que no tengan datos asociados
    """if not estadisticasPeriodo.exists():
        messages.error(request, '¡Las fechas coinciden con períodos anteriores. Revise!')
        return redirect('/mostrarDatosHistoricos/')"""
    return render(request, "mostrarDatosHistoricos.html",{"estadisticasPeriodo":estadisticasPeriodo})


def ayuda(request):
    return render(request, 'ayuda.html')


@login_required
def agregarDatos(request):
    if request.method == 'POST':
        id_periodo = request.POST.get('idPeriodo')

        # Verificar si ya existen registros con el mismo idPeriodo
        if EstadisticaPeriodo.objects.filter(idPeriodo=id_periodo).exists():
            messages.error(request,
                           'Ya existen datos guardados para este periodo académico. No se pueden agregar nuevos datos.')
            return redirect('agregarDatos')

        # Validar que todos los campos no estén vacíos
        all_filled = True
        for tipo in ['matriculados', 'aprobados', 'reprobados', 'desertores', 'foraneos']:
            for i in range(1, 9):
                if not request.POST.get(f'{tipo}_{i}', ''):
                    all_filled = False
                    break
            if not all_filled:
                break

        if not all_filled:
            messages.error(request, 'Todos los campos deben ser llenados. No se pueden dejar campos vacíos.')
            return redirect('agregarDatos')

        # Guardar el registro con los datos totales asociados al idPeriodo
        total_matriculados = sum(int(request.POST.get(f'matriculados_{i}', 0)) for i in range(1, 9))
        total_aprobados = sum(int(request.POST.get(f'aprobados_{i}', 0)) for i in range(1, 9))
        total_reprobados = sum(int(request.POST.get(f'reprobados_{i}', 0)) for i in range(1, 9))
        total_desertores = sum(int(request.POST.get(f'desertores_{i}', 0)) for i in range(1, 9))
        total_foraneos = sum(int(request.POST.get(f'foraneos_{i}', 0)) for i in range(1, 9))

        estadistica_total = EstadisticaPeriodo(
            numMatriculados=total_matriculados,
            numAprobados=total_aprobados,
            numReprobados=total_reprobados,
            numDesertores=total_desertores,
            numForaneos=total_foraneos,
            idPeriodo=PeriodoAcademico.objects.get(id=id_periodo),
            idAdministrador=request.user
        )
        estadistica_total.save()

        # Obtener ciclos asociados con el idPeriodo
        ciclos = Ciclo.objects.filter(idPeriodo_id=id_periodo)

        # Crear los registros para cada ciclo asociado al idPeriodo
        for ciclo in ciclos:
            ciclo_numero = ciclo.numero
            num_matriculados = request.POST.get(f'matriculados_{ciclo_numero}', 0)
            num_aprobados = request.POST.get(f'aprobados_{ciclo_numero}', 0)
            num_reprobados = request.POST.get(f'reprobados_{ciclo_numero}', 0)
            num_desertores = request.POST.get(f'desertores_{ciclo_numero}', 0)
            num_foraneos = request.POST.get(f'foraneos_{ciclo_numero}', 0)

            estadistica_ciclo = EstadisticaPeriodo(
                numMatriculados=num_matriculados,
                numAprobados=num_aprobados,
                numReprobados=num_reprobados,
                numDesertores=num_desertores,
                numForaneos=num_foraneos,
                idCiclo=ciclo,
                idAdministrador=request.user
            )
            estadistica_ciclo.save()

        messages.success(request, 'Datos guardados correctamente.')
        return redirect('agregarDatos')
    else:
        periodos = PeriodoAcademico.objects.all()
        return render(request, 'agregarDatos.html', {'periodos': periodos})