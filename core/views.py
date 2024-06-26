import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse
from .forms import SignupForm, LibroForm, LibroModificacionForm, CustomUserForm, CustomUserModificacionForm
from .models import CategoriaLibro, Libro, CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login

NOMBRE_DEL_SITIO = 'Librotek'
# @login_required
def titulo(subtitulo=None):
    if subtitulo is None:
        return NOMBRE_DEL_SITIO
    return f'{NOMBRE_DEL_SITIO} - {subtitulo}'

# Views
@login_required
def index(request):
    user = request.user
    username = user.username if user.is_authenticated else None
    return render(request, 'core/index.html',
        {
            'titulo': titulo(),
            'subtitulo': ', Bienvenido a Librotek!',
            'username': username
        }
    )

def filtrar_libros(categoria):
    with open('core/libros.json', encoding='utf-8') as file:
        libros = json.load(file)
    libros_filtrados = [libro for libro in libros if libro['categoria'] == categoria]
    return libros_filtrados

def historia(request):
    libros = filtrar_libros('Historia')
    return render(request, 'core/categoria.html', {'libros': libros})

def fantasia(request):
    libros = filtrar_libros('Fantasía')
    return render(request, 'core/categoria.html', {'libros': libros})

def psicologia(request):
    libros = filtrar_libros('Psicología')
    return render(request, 'core/categoria.html', {'libros': libros})

def manuales(request):
    libros = filtrar_libros('Manuales')
    return render(request, 'core/categoria.html', {'libros': libros})

def novelas(request):
    libros = filtrar_libros('Novelas')
    return render(request, 'core/categoria.html', {'libros': libros})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@permission_required('core.view_customuser')
def lista_usuarios(request):
    order_by = request.GET.get('order_by', 'username')
    order_dir = request.GET.get('order_dir', 'asc')

    if order_dir == 'desc':
        order_by = '-' + order_by

    usuarios = CustomUser.objects.order_by(order_by)

    context = {
        'usuarios': usuarios,
        'order_by': order_by,
        'order_dir': order_dir,
    }
    return render(request, 'core/lista_usuarios.html', context)

@permission_required('core.add_customuser')
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            username_usuario = usuario.username
            messages.success(request, f'Usuario "{username_usuario}" creado correctamente.')
            return redirect('/lista/usuarios/')
    else:
        form = CustomUserForm()
    return render(request, 'core/form_usuario.html', {'form': form})

@permission_required('core.change_customuser')
def modificar_usuario(request, usuario_id):
    usuario = get_object_or_404(CustomUser, pk=usuario_id)
    
    if request.method == 'POST':
        form = CustomUserModificacionForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            nueva_contraseña = form.cleaned_data.get('password')
            if nueva_contraseña:
                usuario.set_password(nueva_contraseña)
            usuario.save()
            username_usuario = usuario.username
            messages.success(request, f'Usuario "{username_usuario}" modificado correctamente.')
            return redirect('/')
    else:
        form = CustomUserModificacionForm(instance=usuario)
    
    return render(request, 'core/form_mod_usuario.html', {'form': form})

@permission_required('core.delete_customuser')
def eliminar_usuario(request, usuario_id):
    try:
        usuario = get_object_or_404(CustomUser, id=usuario_id)
        username_usuario = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{username_usuario}" eliminado correctamente.')
    except:
        messages.error(request, 'Error al eliminar el usuario.')
    return redirect('/lista/usuarios/')

@permission_required('core.view_libro')
def lista_libros(request):
    order_by = request.GET.get('order_by', 'categoria__nombre')
    order_dir = request.GET.get('order_dir', 'asc')

    if order_dir == 'desc':
        order_by = '-' + order_by

    libros = Libro.objects.order_by(order_by)

    context = {
        'libros': libros,
        'order_by': order_by,
        'order_dir': order_dir,
    }
    return render(request, 'core/lista_libros.html', context)

@permission_required('core.add_libro')
def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save()
            titulo_libro = libro.titulo
            messages.success(request, f'Libro "{titulo_libro}" creado correctamente.')
            return redirect('/lista/libros/')
    else:
        form = LibroForm()
    return render(request, 'core/form_libro.html', {'form': form})

@permission_required('core.change_libro')
def modificar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    
    if request.method == 'POST':
        form = LibroModificacionForm(request.POST, instance=libro)
        if form.is_valid():
            libro_modificado = form.save(commit=False)
            libro_modificado.save()
            titulo_libro = libro_modificado.titulo
            messages.success(request, f'Libro "{titulo_libro}" modificado correctamente.')
            return redirect('/lista/libros/')
    else:
        form = LibroModificacionForm(instance=libro)
    
    return render(request, 'core/form_mod_libro.html', {'form': form})

@permission_required('core.delete_libro')
def eliminar_libro(request, libro_id):
    try:
        libro = get_object_or_404(Libro, id=libro_id)
        titulo_libro = libro.titulo
        libro.delete()
        messages.success(request, f'Libro "{titulo_libro}" eliminado correctamente.')
    except:
        messages.error(request, 'Error al eliminar el libro.')
    return redirect('/lista/libros/')