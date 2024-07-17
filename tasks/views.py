from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import UsuarioForm
from .models import Usuario, Cuenta, Rol
from django.contrib import messages

import tasks.RungeKutta as r
from django.http.response import JsonResponse

def home(request):
    return render(request, 'home.html')

def iniciarSesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            cuenta = Cuenta.objects.get(correo=username)
            if cuenta.check_password(password):
                request.session['user_id'] = cuenta.id
                if cuenta.rol_id == 1:
                    return redirect('homeAdministrador')
                else:
                    return redirect('homePersonal')
            else:
                error = 'Credenciales inválidas'
        except Cuenta.DoesNotExist:
            error = 'Cuenta no existe'

        return render(request, 'iniciarSesion.html', {'error': error})

    return render(request, 'iniciarSesion.html')


def registrarUsuario(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                usuario = Usuario.objects.create(
                    dni=request.POST['dni'],
                    nombres=request.POST['nombres'],
                    apellidos=request.POST['apellidos'],
                    direccion=request.POST['direccion'],
                    telefono=request.POST['telefono']
                )
                nombre_rol = request.POST['tipo_cargo']
                if nombre_rol == "Personal Administrativo":
                    rol = Rol.objects.get(nombre='Personal Admvo')
                elif nombre_rol == "Administrador":
                    rol = Rol.objects.get(nombre='Administrador')
                cuenta = Cuenta.objects.create(
                    correo=request.POST['correo'],
                    estado=True,
                    rol=rol,
                    usuario=usuario
                )
                cuenta.set_password(request.POST['dni'])
                cuenta.save()
                messages.success(request, 'Usuario registrado correctamente!')
                return redirect('admiManage')
        except IntegrityError:
            messages.error(request, 'El correo ya está registrado.')
            return redirect('admiManage')

        except Exception as e:
            print("Error:", e)
            messages.error(request, f'Error al registrar usuario: {e}')
            return redirect('admiManage')

    return render(request, 'admiManage.html')


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


def eliminarUsuario(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return redirect('admiManage')


def ordenarUsuarios(request):
    listaU = Usuario.objects.all().order_by('nombres')
    print(listaU)
    messages.success(request, '!Lista ordenada!')
    return render(request, "manageUser.html", {"usuarios": listaU})


def manage_user(request):
    usuarios = Usuario.objects.all()
    return render(request, "manageUser.html", {"usuarios": usuarios})


def admiManage(request):
    personalAdministrativo = Usuario.objects.all()
    return render(request, 'admiManage.html', {"personalAdministrativo": personalAdministrativo})

def homeAdministrador(request):
    return render(request, 'homeAdministrador.html')

def perfilAdministrador(request):
    return render(request, 'perfilAdministrador.html')

def homePersonal(request):
    return render(request, 'homePersonal.html')

def graficaPrediccion(request):
    tiempo = r.lista_tiempo_prediccion()
    matriculados = r.lista_matriculados_prediccion()
    aprobados = r.lista_aprobados_prediccion()
    reprobados = r.lista_reprobados_prediccion()
    desertores = r.lista_desertores_prediccion()
    foraneos = r.lista_foraneos_prediccion()
    contexto = {'tiempo': tiempo, 'matriculados': matriculados, 'aprobados': aprobados, 'reprobados': reprobados, 'desertores': desertores, 'foraneos': foraneos}
    return render(request, 'InterfazPrediccion.html', contexto)

def index(request):   
    return render(request,'InterfazPrediccion.html')

def datosHistoricos(request):
    tiempo = r.lista_tiempo_prediccion()
    matriculados = r.lista_matriculados_prediccion()
    aprobados = r.lista_aprobados_prediccion()
    reprobados = r.lista_reprobados_prediccion()
    desertores = r.lista_desertores_prediccion()
    foraneos = r.lista_foraneos_prediccion()
    contexto = {'tiempo': tiempo, 'matriculados': matriculados, 'aprobados': aprobados, 'reprobados': reprobados, 'desertores': desertores, 'foraneos': foraneos}
    return render(request, 'datosHistoricos.html', contexto)

def get_chart(request):
    listaD = r.lista_desertores_prediccion()
    listaT = r.lista_tiempo_prediccion()
    listaA = r.lista_aprobados_prediccion()
    listaR = r.lista_reprobados_prediccion()
    listaM = r.lista_matriculados_prediccion()
    listaF = r.lista_foraneos_prediccion()
    tiempoI = min(listaT)
    tiempoF = r.tiempo_final_historico()
    chart={
        'xAxis': [
            {
                'type': 'category',
                'data': listaT
            }
        ],
        'yAxis': [
            {
                'type': "value"
            }
        ],
        
        'title': [
            {
                'text': 'Grafica Prediccion',
                'bottom':  '92%'
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
        'series': [
            {
                'name': 'Foraneos',
                'type': "line",
                'smooth': True,
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': listaF,
                                  
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
                'smooth': True,           
            },
        ]
    }
    return JsonResponse(chart)