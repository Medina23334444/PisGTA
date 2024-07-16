from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import UsuarioForm
from .models import Usuario, Cuenta, Rol
from django.contrib import messages


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