from rest_framework import serializers
from .models import Usuario
#PARA CREAR UN USUARIO NORMAL 
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'nombre', 'apellido', 'num_doc', 'tipo_doc', 'correo', 'password', 'genero', 'cargo', 'estudioF')
        extra_kwargs = {
            'password': {'write_only': True}  # <- para que no aparezca en GET
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Usuario(**validated_data)
        if password:
            user.set_password(password)  # <- asegura que se encripte
        user.save()
        return user
