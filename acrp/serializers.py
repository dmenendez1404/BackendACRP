from rest_framework import serializers, exceptions
from .models import *
from django.contrib.auth import authenticate


class CentroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Centro
        fields = ('url', 'id', 'nombre', 'logo', 'direccion')


class UserSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedRelatedField(view_name='api:userprofile-detail', source='miembro')
    class Meta:
        model = User
        fields = ('url', 'id',
                  'first_name',
                  'last_name',
                  'username',
                  'password',
                  'email',
                  'is_staff',
                  'is_active',
                  'date_joined')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "Usuario inactivo"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "No existe el usuario"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Incorrecto"
            raise exceptions.ValidationError(msg)
        return data


class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = (
            'url',
            'id',
            'titulo',
            'categoria',
            'pdf',
            'autores')


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = (
            'url',
            'id',
            'titulo',
            'categoria',
            'pdf',
            'miembros')


class EventoSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(EventoSerializer, self).__init__(*args, **kwargs)
        request = kwargs['context']['request']
        if request.method != 'PUT' and request.method != 'POST':
            self.fields['centro'] = CentroSerializer()

    class Meta:
        model = Evento
        fields = (
            'url',
            'id',
            'nombre',
            'categoria',
            'direccion',
            'centro',
            'fecha')


class MiembroSerializer(serializers.ModelSerializer):
    # usuario = UserSerializer()
    def __init__(self, *args, **kwargs):
        super(MiembroSerializer, self).__init__(*args, **kwargs)
        request = kwargs['context']['request']
        if request.method != 'PUT' and request.method != 'POST':
            self.fields['centro'] = CentroSerializer()
            self.fields['proyectos'] = ProyectoSerializer(context={'request': request},many=True)
            self.fields['publicaciones'] = PublicacionSerializer(context={'request': request},many=True)

    class Meta:
        model = Miembro
        fields = ('url', 'id',
                  'activo',
                  'centro',
                  'usuario',
                  'categoria',
                  'resumenCV',
                  'foto',
                  'proyectos',
                  'publicaciones',
                  )
