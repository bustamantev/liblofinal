
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls'),),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name="signup"),
    path('lista/usuarios/', views.lista_usuarios, name="userlist"),
    path('form-usuario/', views.crear_usuario, name="userform"),
    path('modificar-usuario/<int:usuario_id>/', views.modificar_usuario, name='modificar-usuario'),
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar-usuario'),
    path('lista/libros/', views.lista_libros, name="booklist"),
    path('form-libro/', views.crear_libro, name="bookform"),
    path('modificar-libro/<int:libro_id>/', views.modificar_libro, name='modificar-libro'),
    path('eliminar-libro/<int:libro_id>/', views.eliminar_libro, name='eliminar-libro'),
    path('historia/', views.historia, name="historia"),
    path('fantasia/', views.fantasia, name="fantasia"),
    path('manuales/', views.manuales, name="manuales"),   
    path('novelas/', views.novelas, name="novelas"),
    path('psicologia/', views.psicologia, name="psicologia"),
    path('api/', include('api_rest.urls')),
    # URLS incluidas:  /api/categorias/ y /api/libros/
]
