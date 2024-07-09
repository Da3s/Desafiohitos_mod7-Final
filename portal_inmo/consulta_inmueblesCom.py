import os
import django
from django.db.models import Prefetch


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_inmo.settings')
django.setup()

from gestion.models import Propiedad


def consulta_inmueblesCom():

    inmuebles_por_comuna = Propiedad.objects.values('comuna__nombre', 'nombre', 'descripcion').order_by('comuna__nombre')

    with open('inmuebles_por_comuna.txt', 'w') as file:
        comuna_actual = None
        for inmueble in inmuebles_por_comuna:
            if inmueble['comuna__nombre'] != comuna_actual:
                comuna_actual = inmueble['comuna__nombre']
                file.write(f"\nComuna: {comuna_actual}\n")
                file.write("-" * 30 + "\n")
            file.write(f"Nombre: {inmueble['nombre']}\n")
            file.write(f"Descripción: {inmueble['descripcion']}\n")
            file.write("\n")

if __name__ == '__main__':
    consulta_inmueblesCom()
