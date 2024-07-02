from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Tipo_usuario(models.Model):
    nombre = models.CharField(max_length=20, primary_key=True)
    
    def __str__(self):
        return self.nombre
    

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, null= False)
    rut= models.CharField(max_length=9)
    nombre = models.CharField(max_length=100, null=False, blank= False)
    apellidos = models.CharField(max_length=100, null=False, blank= False)
    direccion = models.CharField(max_length=150, null=False, blank= False)
    telefono = models.CharField(max_length=30, null=False, blank= False)
    correo_electronico = models.EmailField(max_length=100, unique=True, null=False, blank= False)
    tipo_usuario = models.ForeignKey(Tipo_usuario, on_delete=models.CASCADE, null= False)
    
    def __str__(self):
        return self.nombre


class Tipo_propiedad(models.Model):
    nombre = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombre
    
    
class Region(models.Model):
    nombre = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombre
    
    
class Comuna(models.Model):
    nombre = models.CharField(max_length=20)
    region= models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.nombre
    
    
class Propiedad(models.Model):
    nombre = models.CharField(max_length=100, null= False, blank= False)
    descripcion = models.TextField()
    m2_construidos = models.FloatField(null= False)
    m2_totales = models.FloatField(null= False)
    cantidad_estacionamientos = models.IntegerField(default= 0)
    cantidad_habitaciones = models.IntegerField(default= 0)
    cantidad_banios = models.IntegerField(default= 0)
    direccion = models.CharField(max_length=150, null= False, blank= False)
    precio_mensual = models.IntegerField(null= False)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)    
    tipo_propiedad = models.ForeignKey(Tipo_propiedad, on_delete=models.CASCADE, null= False)
    arrendador = models.ForeignKey(User, on_delete= models.CASCADE, null= False)
    arrendatario = models.ForeignKey(Usuario, on_delete= models.CASCADE, null= True)
    arrendada = models.BooleanField(default= False)
    
    def __str__(self):
        return self.nombre
    
    
class SolicitudArriendo(models.Model):
    arrendatario = models.ForeignKey(User, on_delete=models.CASCADE)
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')
    
    
    def __str__(self):
        return self.propiedad
    