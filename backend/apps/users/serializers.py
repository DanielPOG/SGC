"""
    Serializers app users
"""
from apps.cargos.models import Cargos #pylint:disable=import-error
from apps.formacion.models import EstudioFormal #pylint:disable=import-error
from rest_framework import serializers
from .models import Usuarios, TiposDoc, Generos #pylint:disable=relative-beyond-top-level
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import string, secrets
import os
from django.conf import settings
from email.mime.image import MIMEImage

def generar_password(longitud=12):
    """Genera una contraseña aleatoria segura"""
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

class TipoDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposDoc
        fields = ['id', 'tipo', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generos
        fields = ['id', 'sigla', 'nombre', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UsuarioSerializer(serializers.ModelSerializer):
    tipo_doc = serializers.SlugRelatedField(
        slug_field='id',
        queryset=TiposDoc.objects.all()
    )
    genero = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Generos.objects.all()
    )
    cargo = serializers.PrimaryKeyRelatedField(queryset=Cargos.objects.all())
    estudio_formal = serializers.PrimaryKeyRelatedField(queryset=EstudioFormal.objects.all())
    class Meta:
        model = Usuarios
        fields = [
            'id', 'nombre', 'apellido', 'num_doc', 
            'tipo_doc', 'genero', 'username', 
            'cargo', 'estudio_formal', 'fecha_ingreso',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    def validate_email(self, value):
        if not value.endswith('@soy.sena.edu.co'):
            raise serializers.ValidationError(
                "El correo debe ser institucional @soy.sena.edu.co"
            )
        return value
    def send_custom_email(self, user, password):
        subject = 'Activación de Usuario <Sistema de Gestión de Cargos>'
        from_email = 'jdmapple322@gmail.com'
        to=[user.username]
        
        context = {"usuario":user.username, "password":password}
        html_content = render_to_string('email/activacion.html', context)
        msg = EmailMultiAlternatives(subject, "", from_email, to)
        msg.attach_alternative(html_content, 'text/html')
        
        logo_path = os.path.join(settings.BASE_DIR, "static", "logo.png")
        with open(logo_path, "rb") as f:
            logo = MIMEImage(f.read())
            logo.add_header('Content-ID', '<logo>')
            logo.add_header('Content-Disposition', 'inline', filename="logo.png")
            msg.attach(logo)
        
        msg.send()
    
    
    def create(self, validate_data):
        usuario = Usuarios.objects.create(**validate_data)
        password = generar_password(12)
        usuario.set_password(password)
        usuario.save()
        # Enviar correo
        self.send_custom_email(usuario, password)
        return usuario
