from django import forms
from .models import Usuario, Perfil


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombres", "apellidos", "direccion", "telefono"]


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["fotoPerfil", "descripcion", "usuarioInstagram", "usuarioFacebook", "usuarioTwitter"]