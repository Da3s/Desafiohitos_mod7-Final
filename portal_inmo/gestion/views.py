from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .services import *
from .forms import *
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
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']

        user = request.user
        user.username = username
        user.email = email
        user.save()

        usuario.nombre = nombre
        usuario.apellidos = apellidos
        usuario.direccion = direccion
        usuario.telefono = telefono
        usuario.correo_electronico = email
        usuario.save()

        messages.success(request, 'Los datos se actualizaron correctamente.')
        return redirect('indice')

    context = {
        'usuario': usuario,
        'nombre_usuario': request.user.username,
        'tipo_usuario': usuario.tipo_usuario.nombre,
    }
    return render(request, 'actualizar_usuario.html', context)


############################ Vistas arrendatario ##################################

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
        comunas = comunas.filter(region_id=region_id)  

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


############################ Fin Vistas arrendatario ##################################


################################## Vistas Arrendador ###########################################


# Publicar propiedad como Arrendador

def is_arrendador(user):
    return user.is_authenticated and hasattr(user, 'usuario') and user.usuario.tipo_usuario.nombre == 'Arrendador'

@login_required
@user_passes_test(is_arrendador)
def publicar_propiedad(request):
    regiones = Region.objects.all()
    region_seleccionada = request.POST.get('region') if request.method == 'POST' else request.GET.get('region')
    comunas = Comuna.objects.filter(region_id=region_seleccionada) if region_seleccionada else Comuna.objects.none()

    if request.method == 'POST':
        form = PropiedadForm(request.POST)
        if form.is_valid():
            nueva_propiedad = form.save
            nueva_propiedad.arrendador = request.user
            nueva_propiedad.save()
            return redirect('detalle_propiedad', pk=nueva_propiedad.pk)
    else:
        form = PropiedadForm()

    tipos_propiedad = Tipo_propiedad.objects.all()
    context = {
        'form': form,
        'regiones': regiones,
        'comunas': comunas,
        'tipos_propiedad': tipos_propiedad,
        'region_seleccionada': region_seleccionada,
    }
    return render(request, 'publicar_propiedad.html', context)




# Vista detalle de propiedades

def detalle_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    return render(request, 'detalle_propiedad.html', {'propiedad': propiedad})


# Vista Dashboard

def is_arrendador(user):
    return user.is_authenticated and hasattr(user, 'usuario') and user.usuario.tipo_usuario.nombre == 'Arrendador'

@login_required
@user_passes_test(is_arrendador)
def dashboard_propiedades(request):

    propiedades = Propiedad.objects.filter(arrendador=request.user)

    if request.method == 'POST':

        if 'delete' in request.POST:
            propiedad_id = request.POST.get('propiedad_id')
            if propiedad_id:
                propiedad = get_object_or_404(Propiedad, pk=propiedad_id)
                propiedad.delete()
                return redirect('dashboard_propiedades')
        elif 'edit' in request.POST:
            propiedad_id = request.POST.get('propiedad_id')
            if propiedad_id:
                propiedad = get_object_or_404(Propiedad, pk=propiedad_id)
                form = PropiedadForm(request.POST, instance=propiedad)
                if form.is_valid():
                    form.save()
                    return redirect('dashboard_propiedades')
            else:
                form = PropiedadForm()

    else:
        form = PropiedadForm()

    return render(request, 'dashboard_propiedades.html', {'propiedades': propiedades, 'form': form})




# Vista editar propiedad

def is_arrendador(user):
    return user.is_authenticated and hasattr(user, 'usuario') and user.usuario.tipo_usuario.nombre == 'Arrendador'

@login_required
@user_passes_test(is_arrendador)
def editar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)

    if request.method == 'POST':
        form = PropiedadForm(request.POST, instance=propiedad)
        if form.is_valid():
            form.save()
            return redirect('detalle_propiedad', pk=pk)
    else:
        form = PropiedadForm(instance=propiedad)

    return render(request, 'editar_propiedad.html', {'form': form, 'propiedad': propiedad})



# Vista para que arrendador pueda ver solicitudes

def is_arrendador(user):
    return user.is_authenticated and hasattr(user, 'usuario') and user.usuario.tipo_usuario.nombre == 'Arrendador'

@login_required
@user_passes_test(is_arrendador)
def solicitudes_arriendo(request):
    arrendador = request.user 
    solicitudes_pendientes = SolicitudArriendo.objects.filter(propiedad__arrendador=arrendador, estado='pendiente')
    return render(request, 'solicitudes_arriendo.html', {'solicitudes': solicitudes_pendientes})



# Vista para gestionar solicitudes

# Aceptar

def is_arrendador(user):
    return user.is_authenticated and hasattr(user, 'usuario') and user.usuario.tipo_usuario.nombre == 'Arrendador'

@login_required
@user_passes_test(is_arrendador)
def aceptar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudArriendo, pk=solicitud_id)
    solicitud.estado = 'aceptada'
    solicitud.save()
    return redirect('solicitudes_arriendo')


# Rechazar

def is_arrendador(user):
    return user.is_authenticated and hasattr(user, 'usuario') and user.usuario.tipo_usuario.nombre == 'Arrendador'

@login_required
@user_passes_test(is_arrendador)
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudArriendo, pk=solicitud_id)
    solicitud.estado = 'rechazada'
    solicitud.save()
    return redirect('solicitudes_arriendo')


################################## Fin Vistas Arrendador ###########################################