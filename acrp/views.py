from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import UpdateAPIView
from acrp.serializers import *

from rest_framework.permissions import IsAuthenticated

from rest_framework.permissions import IsAuthenticatedOrReadOnly


class MiembroViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer


class JuntaDirectivaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = Miembro.objects.exclude(cargo='')
    serializer_class = MiembroSerializer


class ProyectoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer


class PublicacionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer


class MensajeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer


class BoletinViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = Boletin.objects.all()
    serializer_class = BoletinSerializer


class CentroViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = Centro.objects.all()
    serializer_class = CentroSerializer


class NoticiaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer


class EventoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @api_view(['POST'])
    def create_user(request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateMiembroViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]
    queryset = Miembro.objects.all()
    serializer_class = UpdateMiembroSerializer

from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class MyAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        member = Miembro.objects.get(usuario=user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'miembro_id': member.pk,
        })
