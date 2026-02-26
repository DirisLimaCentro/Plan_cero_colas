 

from django.urls import path
from .views import registrar_cita, obtener_servicios

urlpatterns = [
    path('registrar-cita/', registrar_cita, name='registrar_cita'),
    path('api/servicios/', obtener_servicios, name='obtener_servicios'),
]