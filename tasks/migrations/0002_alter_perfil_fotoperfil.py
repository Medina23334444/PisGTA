# Generated by Django 5.0.7 on 2024-08-01 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='fotoPerfil',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes'),
        ),
    ]