from django.test import TestCase
from django.utils import timezone

# models test
from acrp.models import *


class CentroTest(TestCase):

    def create_centro(self, nombre="UCI",
                        direccion="Km 2½ Autopista La Habana - San Antonio de los Baños, La Habana, Cuba",
                        activo=True):
        return Centro.objects.create(nombre=nombre, direccion=direccion, activo=activo)

    def test_centro_creation(self):
        c = self.create_centro()
        self.assertTrue(isinstance(c, Centro))
        self.assertEqual(c.__str__(), c.nombre)