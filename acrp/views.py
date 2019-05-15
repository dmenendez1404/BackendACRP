from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken

from acrp.serializers import *

from rest_framework.permissions import IsAuthenticated


class MiembroViewSet(viewsets.ModelViewSet):
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer

class JuntaDirectivaViewSet(viewsets.ModelViewSet):
    queryset = Miembro.objects.exclude(cargo='')
    serializer_class = MiembroSerializer

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer


class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer

class BoletinViewSet(viewsets.ModelViewSet):
    queryset = Boletin.objects.all()
    serializer_class = BoletinSerializer


class CentroViewSet(viewsets.ModelViewSet):
    queryset = Centro.objects.all()
    serializer_class = CentroSerializer


class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class MyAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        member = Miembro.objects.get(usuario=user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'miembro_id': member.pk,
        })
