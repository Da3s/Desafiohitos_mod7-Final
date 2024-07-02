import os
import json
from django.core.wsgi import get_wsgi_application
from gestion.models import Region, Comuna

def cargar_datos_desde_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        regiones = data['Regiones']
        
        for region_data in regiones:
            nombre_region = region_data['nombre']
            region, created = Region.objects.get_or_create(nombre=nombre_region)
            
            comunas = region_data['Comunas']
            for comuna_data in comunas:
                nombre_comuna = comuna_data['nombre']
                Comuna.objects.get_or_create(nombre=nombre_comuna, region=region)

if __name__ == '__main__':
    # Ruta real al archivo JSON, teniendo en cuenta que está en la carpeta 'static/js'
    file_path = os.path.join(os.path.dirname(__file__), 'static/js/com_reg.json')
    cargar_datos_desde_json(file_path)
    print('Datos cargados exitosamente.')