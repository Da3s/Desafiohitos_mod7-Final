from django.contrib.auth.models import User
from .models import Usuario, Propiedad, Comuna, Tipo_usuario, Tipo_propiedad, Region
from .forms import *




def listar_propiedades():
    propiedades = Propiedad.objects.all()
    return propiedades


def registrar_usuario(username, password, email, rut, nombre, apellidos, direccion, telefono, tipo_usuario_nombre):
    user = User.objects.create_user(username=username, password=password, email=email)
    tipo_usuario = Tipo_usuario.objects.get(nombre=tipo_usuario_nombre)
    usuario = Usuario.objects.create(
        user=user,
        rut=rut,
        nombre=nombre,
        apellidos=apellidos,
        direccion=direccion,
        telefono=telefono,
        correo_electronico=email,
        tipo_usuario=tipo_usuario
    )
    return usuario


def actualizar_usuario(user_id, rut, nombre, apellidos, direccion, telefono, email, tipo_usuario_nombre):
    user = User.objects.get(id=user_id)
    tipo_usuario = Tipo_usuario.objects.get(nombre=tipo_usuario_nombre)
    Usuario.objects.filter(user=user).update(
        rut=rut,
        nombre=nombre,
        apellidos=apellidos,
        direccion=direccion,
        telefono=telefono,
        correo_electronico=email,
        tipo_usuario=tipo_usuario
    )
    user.email = email
    user.save()
    return Usuario.objects.get(user=user)


def publicar_propiedad(datos_propiedad):
    form = PropiedadForm(datos_propiedad)
    if form.is_valid():
        nueva_propiedad = form.save()
        return nueva_propiedad
    else:
        print(form.errors)
        return None