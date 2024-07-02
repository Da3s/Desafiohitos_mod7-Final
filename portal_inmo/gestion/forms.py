from .models import *
from django import forms

class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['mensaje']
        
        
        
class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'cantidad_estacionamientos', 
                  'cantidad_habitaciones', 'cantidad_banios', 'direccion', 'precio_mensual', 'region' ,
                  'comuna', 'tipo_propiedad']