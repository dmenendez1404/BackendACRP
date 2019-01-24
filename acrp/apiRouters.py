
from rest_framework import routers

from acrp.views import *

router = routers.DefaultRouter()
router.register(r'miembro', MiembroViewSet)
router.register(r'proyecto', ProyectoViewSet)
router.register(r'publicacion', PublicacionViewSet)
router.register(r'centro', CentroViewSet)
router.register(r'evento', EventoViewSet)