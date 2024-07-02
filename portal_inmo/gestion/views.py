from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .services import registrar_usuario
from .forms import SolicitudArriendoForm
from .models import *

# Create your views here.


# Vista index

def indice(request):
    context = {
        'nombre' : 'Daniel',
        'apellido' : 'Moreno',
    }
    
    return render(request, 'index.html', context)



# Vista para registro de nuevos usuarios

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        password_confirm = request.POST['password2']
        email = request.POST['email']
        rut = request.POST['rut']
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        tipo_usuario_nombre = request.POST['tipo_usuario']
        
        if password == password_confirm:
            try:
                registrar_usuario(username, password, email, rut, nombre, apellidos, direccion, telefono, tipo_usuario_nombre)
                messages.success(request, 'Usuario registrado exitosamente.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error al registrar el usuario: {e}')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
    
    context = {
        'tipos_usuario': Tipo_usuario.objects.all()
    }
    
    return render(request, 'registro.html', context)



# Vista para actualizar datos de usuario

@login_required
def actualizar_usuario(request):
    
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
        return redirect('indice')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        rut = request.POST['rut']
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        tipo_usuario_nombre = request.POST['tipo_usuario']

        try:
            tipo_usuario = Tipo_usuario.objects.get(nombre=tipo_usuario_nombre)
        except Tipo_usuario.DoesNotExist:
            messages.error(request, 'El tipo de usuario no existe.')
            return redirect('actualizar_usuario')

        # Actualizar los datos del usuario de Django
        user = request.user
        user.username = username
        user.email = email
        user.save()

        # Actualizar los datos del modelo Usuario
        usuario.rut = rut
        usuario.nombre = nombre
        usuario.apellidos = apellidos
        usuario.direccion = direccion
        usuario.telefono = telefono
        usuario.correo_electronico = email
        usuario.tipo_usuario = tipo_usuario
        usuario.save()

        messages.success(request, 'Los datos se actualizaron correctamente.')
        return redirect('indice') 

    context = {
        'usuario': usuario,
        'tipos_usuario': Tipo_usuario.objects.all()
    }
    return render(request, 'actualizar_usuario.html', context)


# Listar propiedades

def is_arrendatario(user):
    return user.is_authenticated and hasattr(user, 'usuario') and user.usuario.tipo_usuario.nombre == 'Arrendatario'

@user_passes_test(is_arrendatario)
def listar_propiedades(request):
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    propiedades = Propiedad.objects.all()

    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')

    if region_id:
        propiedades = propiedades.filter(region_id=region_id)
        comunas = comunas.filter(region_id=region_id)  # Filtra las comunas basadas en la región seleccionada

    if comuna_id:
        propiedades = propiedades.filter(comuna_id=comuna_id)

    context = {
        'propiedades': propiedades,
        'regiones': regiones,
        'comunas': comunas,
        'selected_region': region_id,
        'selected_comuna': comuna_id,
    }
    return render(request, 'listar_propiedades.html', context)




# Solicitud de arriendo

def is_arrendatario(user):
    return user.is_authenticated and hasattr(user, 'usuario') and user.usuario.tipo_usuario.nombre == 'Arrendatario'

@login_required
@user_passes_test(is_arrendatario)
def solicitud_arriendo(request, propiedad_id):
    propiedad = Propiedad.objects.get(id=propiedad_id)

    if request.method == 'POST':
        form = SolicitudArriendoForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.arrendatario = request.user
            solicitud.propiedad = propiedad
            solicitud.save()
            return redirect('listar_propiedades')
    else:
        form = SolicitudArriendoForm()

    context = {
        'form': form,
        'propiedad': propiedad,
    }
    return render(request, 'solicitud_arriendo.html', context)