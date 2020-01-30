from django.test import TestCase
from api.tasks import *


# Create your tests here.
class TaskTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_getQuantidadeVendas(self):
        getQuantidadeVendas()