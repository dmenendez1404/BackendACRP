from rest_framework import serializers, exceptions
from .models import *
from django.contrib.auth import authenticate


class CentroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Centro
        fields = ('url', 'id', 'nombre', 'logo', 'direccion', 'activo')


class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = ('url', 'id', 'titulo', 'imagen', 'categoria', 'descripcion')

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
    # def __init__(self, *args, **kwargs):
    #     super(PublicacionSerializer, self).__init__(*args, **kwargs)
    #     request = kwargs['context']['request']
    #     if request.method != 'PUT' and request.method != 'POST':

    # self.fields['autores'] = MiembroSerializer(context={'request': request},many=True)
    class Meta:
        model = Publicacion
        fields = (
            'url',
            'id',
            'titulo',
            'categoria',
            'pdf',
            'descripcion',
            'fecha',
            'autores')


class BoletinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Boletin
        fields = (
            'url',
            'id',
            'titulo',
            'fecha',
            'pdf',
            'descripcion',
            'autores')


class ProyectoSerializer(serializers.ModelSerializer):
    # def __init__(self, *args, **kwargs):
    #     super(ProyectoSerializer, self).__init__(*args, **kwargs)
    #     request = kwargs['context']['request']
    #     if request.method != 'PUT' and request.method != 'POST':
    #         self.fields['miembros'] = MiembroSerializer(context={'request': request},many=True)
    class Meta:
        model = Proyecto
        fields = (
            'url',
            'id',
            'titulo',
            'categoria',
            'pdf',
            'descripcion',
            'miembros')

class MensajeSerializer(serializers.ModelSerializer):
   class Meta:
        model = Mensaje
        fields = (
            'url',
            'id',
            'nombreRemitente',
            'correoRemitente',
            'telefonoRemitente',
            'fecha',
            'mensaje',
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
            'descripcion',
            'fecha')

class MiembroSerializer(serializers.ModelSerializer):
    # usuario = UserSerializer()
    def __init__(self, *args, **kwargs):
        super(MiembroSerializer, self).__init__(*args, **kwargs)
        request = kwargs['context']['request']
        if request.method != 'PUT' and request.method != 'POST':
            self.fields['centro'] = CentroSerializer()
            self.fields['usuario'] = UserSerializer(context={'request': request})
            self.fields['proyectos'] = ProyectoSerializer(context={'request': request}, many=True)
            self.fields['publicaciones'] = PublicacionSerializer(context={'request': request}, many=True)
            self.fields['boletines'] = BoletinSerializer(context={'request': request}, many=True)
            self.fields['mensajes'] = MensajeSerializer(context={'request': request}, many=True)

    class Meta:
        model = Miembro
        fields = ('url', 'id',
                  'activo',
                  'centro',
                  'usuario',
                  'categoria',
                  'cargo',
                  'resumenCV',
                  'foto',
                  'proyectos',
                  'publicaciones',
                  'mensajes',
                  'rol')

class RegistrarMiembroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Miembro
        fields = ('url', 'id',
                  'activo',
                  'centro',
                  'categoria',
                  'cargo',
                  'resumenCV',
                  'foto',
                  )

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        request = kwargs['context']['request']
        if request.method == 'PUT' or request.method == 'POST':
            self.fields['miembro'] = RegistrarMiembroSerializer(context={'request': request})

    def create(self, validated_data, instance=None):
        miembro = validated_data.pop('miembro')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Miembro.objects.create(usuario=user, **miembro)
        return user

    def update(self, instance, validated_data):
        Miembro.objects.update(**validated_data['miembro'])
        User.objects.update(**validated_data)
        print("hey")
        return instance

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
                  'date_joined',
                  'miembro')