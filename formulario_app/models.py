from datetime import date
from django.db import models 
from django.utils.translation import gettext_lazy as _
 


CARGO=((1, 'JEFE (A)'),
             (2, 'SECRETARIA(O)'),
             (3, 'COORDINADOR(A)'),
              (4, 'OTROS') )
              



TIPO_INCIDENCIA=((1, 'Problemas con computadoras'),
                    (2, 'Problemas con Sistemas Institucionales (SIAF, SIGA, SGD, TRAMITE, etc) '),
                    (3, 'Conectividad y Redes'),
                    (4, 'Impresoras y escáner'),
                        (5, 'Software de Ofimática (Word, Excel, etc)'),
                        (6, 'Problemas con SIHCE') )


ESTADOS_RECLAMO = (
    (1, 'Registrado'),
    (2, 'En proceso'),
    (3, 'Atendido'),
    (4, 'Cerrado'),
)



from django.db import models

class Cita(models.Model):
    tipo_documento = models.CharField(max_length=30, null=False, blank=False)
    numero_doc = models.CharField(max_length=20, null=False, blank=False)
    fecha_nacimiento = models.CharField(max_length=15, null=False, blank=False)
    establecimiento = models.CharField(max_length=150, null=False, blank=False)
    ups = models.CharField(max_length=150, null=False, blank=False)
    servicio = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        db_table = 'citas'  # Apunta exactamente a la tabla en MySQL

    def __str__(self):
        return f"{self.tipo_documento} - {self.numero_doc}"
