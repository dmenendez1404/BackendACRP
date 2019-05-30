from rest_framework import routers

from acrp.views import *

router = routers.DefaultRouter()
router.register(r'miembro', MiembroViewSet, 'miembro')
router.register(r'updateMiembro', UpdateMiembroViewSet, 'updateMiembro')
router.register(r'juntaDirectiva', JuntaDirectivaViewSet, 'juntaDirectiva')
router.register(r'proyecto', ProyectoViewSet)
router.register(r'publicacion', PublicacionViewSet)
router.register(r'boletin', BoletinViewSet)
router.register(r'centro', CentroViewSet)
router.register(r'evento', EventoViewSet)
router.register(r'noticia', NoticiaViewSet)
router.register(r'mensaje', MensajeViewSet)
router.register(r'user', UserViewSet, 'user')
