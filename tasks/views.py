from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from django.http import JsonResponse

from .forms import UsuarioForm
from .models import Usuario, Rol, RolPersona, Sugerencia, PeriodoAcademico, Ciclo
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def iniciarSesion(request):
    if request.method == "POST":
        correo = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=correo, password=password)
            if user is not None:
                login(request, user)
                roles_persona = RolPersona.objects.filter(usuario=user)
                roles = [rp.rol for rp in roles_persona]
                print(roles)

                if any(rol.nombre == 'Personal' for rol in roles):
                    return redirect('homePersonal')
                elif any(rol.nombre == 'Administrador' for rol in roles):
                    return redirect('homeAdministrador')
                else:
                    return redirect('homeDefault')
            else:
                error = 'Credenciales inválidas'
                messages.error(request, error)
                return render(request, 'iniciarSesion.html')

        except Exception as e:
            return render(request, 'iniciarSesion.html')

    return render(request, 'iniciarSesion.html')


@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('home')


@login_required
def registrarUsuario(request):
    if request.method == 'POST':
        data = request.POST
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

                print(usuario.username)
                print(usuario.password)

                if data['tipo_cargo'] == 'Administrador':
                    rol = Rol.objects.get(nombre='Administrador')
                elif data['tipo_cargo'] == 'Personal':
                    rol = Rol.objects.get(nombre='Personal')
                else:
                    messages.error(request, 'Tipo de cargo no válido.')
                    return redirect('admiManage')

                RolPersona.objects.create(rol=rol, usuario=usuario)
                print(RolPersona.objects.all())

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


@login_required
def ordenarUsuarios(request):
    listaU = Usuario.objects.all().order_by('nombres')
    print(listaU)
    messages.success(request, '!Lista ordenada!')
    return render(request, "manageUser.html", {"usuarios": listaU})


@login_required
def manage_user(request):
    usuarios = Usuario.objects.all()
    return render(request, "manageUser.html", {"usuarios": usuarios})


@login_required
def admiManage(request):
    personalAdministrativo = Usuario.objects.all()
    return render(request, 'admiManage.html', {"personalAdministrativo": personalAdministrativo})


@login_required
def homeAdministrador(request):
    return render(request, 'homeAdministrador.html')


@login_required
def perfilAdministrador(request):
    return render(request, 'perfilAdministrador.html')


@login_required
def homePersonal(request):
    return render(request, 'homePersonal.html')


"""Métodos de Periodo"""

def mostrarPeriodos(request):#Vista general de Periodos 
    periodos = PeriodoAcademico.objects.all()
    #messages.success(request, '!Lista actualizada!')
    return render(request, "gestionPeriodoHome.html",{"periodos":periodos})

def guardar_editar_Periodos(request):#Vista para editar o agregar 
    periodos = PeriodoAcademico.objects.all()
    #messages.success(request, '!Lista actualizada!')
    return render(request, "gestionPeriodo.html",{"periodos":periodos})

def obtener_eventos(request):#Método para cargar los periodos registrados en calendar
    periodos = PeriodoAcademico.objects.all()
    eventos = []

    for periodo in periodos:
        eventos.append({
            'title': periodo.nombre,
            'start': periodo.fechaInicio.isoformat(),
            #'end': periodo.fechaFin.isoformat(),
            'end': (periodo.fechaFin + timedelta(days=1)).isoformat(),
            'allDay': True,  # Para que se muestre como evento de todo el día
        })

    return JsonResponse(eventos, safe=False)

#@csrf_protect
def registrarPeriodo(request):
    #Se los recibe como strings
    fechaI_str = request.POST.get('fecha_inicio')
    #fechaI = request.POST['fecha_inicio']#atributo name Objeto en HTML
    fechaF_str = request.POST.get('fecha_fin')
    
    #Se los convierte
    fechaI = datetime.strptime(fechaI_str, '%Y-%m-%d').date()
    fechaF = datetime.strptime(fechaF_str, '%Y-%m-%d').date()
    nombreP = PeriodoAcademico.fijarNombre(fechaI,fechaF)

    #Podría analizarse condicional para guardar o editar
    #idP = request.POST['txtId']
    try: #Si puede convertir el id a entero, existe, debe actualizar
        idP = int(request.POST['txtId'])
        periodo = PeriodoAcademico.objects.get(id = idP)
        periodo.fechaInicio = fechaI
        periodo.fechaFin = fechaF
        periodo.nombre = nombreP
        periodo.save()
    except ValueError: #Si devuelve un ID nulo, crear
        periodo = PeriodoAcademico.objects.create(fechaInicio = fechaI, fechaFin = fechaF, nombre = nombreP)
        #Al crear periodo, creo sus ciclos
        #Ver si los ciclos guardo aquí o en la Clase
        for i in range(1,9):
            ciclo = Ciclo.objects.create(idPeriodo = periodo.id, numero = i)

    """if idP is not None and isinstance(idP, int):#Si no es nulo, existe, y es un numero entero debo actualizar
        periodo = PeriodoAcademico.objects.get(id = idP)
        periodo.fechaInicio = fechaI
        periodo.fechaFin = fechaF
        periodo.nombre = nombreP
        periodo.save()
    else:#Si el id es nulo debe crear uno nuevo:
        periodo = PeriodoAcademico.objects.create(fechaInicio = fechaI, fechaFin = fechaF, nombre = nombreP)"""
    
    messages.success(request, '!Periodo guardado correctamente¡')
    return redirect('/')

@login_required
def sugerenciaPersonal(request):
    if request.method == 'POST':
        try:
            sugerencia = Sugerencia.objects.create(
                asunto=request.POST['asunto'],
                descripcion=request.POST['descripcion'],
                usuario=request.user
            )
            messages.success(request, 'Sugerencia enviada con éxito.')
            return redirect('nombre_de_la_vista_a_redirigir')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return render(request, 'tu_template.html')

    return render(request, 'tu_template.html')
