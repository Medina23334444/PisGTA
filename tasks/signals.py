
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Perfil
from datetime import date


@receiver(post_save, sender=Usuario)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(
            usuario=instance,
            fechaNacimiento=date.today(),
            descripcion='',
            usuarioInstagram='',
            usuarioFacebook='',
            usuarioTwitter=''
        )
