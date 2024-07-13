import os
import django
from django.db import connection


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_inmo.settings')
django.setup()

def inmuebles_por_region():
    
    query = """
        SELECT region.nombre AS region_nombre, 
               propiedad.nombre AS propiedad_nombre, 
               propiedad.descripcion,
               propiedad.m2_construidos,
               propiedad.m2_totales,
               propiedad.cantidad_habitaciones,
               propiedad.cantidad_estacionamientos,
               propiedad.cantidad_banios,
               propiedad.direccion,
               propiedad.precio_mensual,
               propiedad.tipo_propiedad_id
        FROM gestion_propiedad AS propiedad
        JOIN gestion_comuna AS comuna ON propiedad.comuna_id = comuna.id
        JOIN gestion_region AS region ON comuna.region_id = region.id
        ORDER BY region.nombre, propiedad.nombre;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        inmuebles_por_region = cursor.fetchall()
    

    with open('inmuebles_por_region.txt', 'w') as file:
        region_actual = None
        for inmueble in inmuebles_por_region:
            (region_nombre, propiedad_nombre, descripcion, m2_construidos, m2_totales, cantidad_habitaciones, 
             cantidad_estacionamientos, cantidad_banios, direccion, precio_mensual, tipo_propiedad) = inmueble
            
            
            if region_nombre != region_actual:
                region_actual = region_nombre
                file.write(f"\nRegión: {region_actual}\n")

                file.write("-" * 30 + "\n")
            
            # Datos que quiero ir escribiendo en el archivo, en este caso todos.
            file.write(f"Nombre: {propiedad_nombre}\n")
            file.write(f"Descripción: {descripcion}\n")
            file.write(f"Dirección: {direccion}\n")
            file.write(f"Precio: {precio_mensual}\n")
            file.write(f"Superficie construida: {m2_construidos} m²\n")
            file.write(f"Superficie total: {m2_totales} m²\n")
            file.write(f"Habitaciones: {cantidad_habitaciones}\n")
            file.write(f"Estacionamientos: {cantidad_estacionamientos}\n")
            file.write(f"Baños: {cantidad_banios}\n")
            file.write(f"Tipo: {tipo_propiedad}\n")
            file.write("\n")

if __name__ == '__main__':
    inmuebles_por_region()
