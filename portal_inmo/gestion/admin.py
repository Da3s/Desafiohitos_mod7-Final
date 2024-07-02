from django.contrib import admin
from .models import Tipo_propiedad, Tipo_usuario, Usuario, Region, Comuna, Propiedad

# Register your models here.

admin.site.register(Tipo_propiedad)
admin.site.register(Tipo_usuario)
admin.site.register(Usuario)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Propiedad)