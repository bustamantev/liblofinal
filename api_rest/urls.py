from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#  PARA OBTENER EL TOKEN ENVIAR LAS CREDENCIALES EN UNA CONSULTA POST
#  EN EL BODY DE LA SIGUIENTE FORMA CAMBIANDO LOS VALORES POR LOS DE UN USUARIO REGISTRADO:
#  {
#     "username": "usuario",
#     "password": "contraseña"
#  }
#  LUEGO ENVIAR EL TOKEN ACCESS COMO BEARER TOKEN

    # APIS PARA OBTENER LA LISTA DE LIBROS Y CATEGORIAS (GET)
    path('libros/', views.LibroList.as_view(), name='libro-list'),
    path('categorias/', views.CategoriaLibroList.as_view(), name='categoria-list'),

    # API PARA CREAR UN NUEVO LIBRO (POST)
    # {
    # "titulo": "Título del libro",
    # "autor": "Autor del libro",
    # "descripcion": "Descripción del libro",
    # "precio": "Precio del libro",
    # "categoria": "ID de la categoria",
    # "src_imagen": "Url de imagen"
    # }
    path('libros/crear/', views.CrearLibro.as_view(), name='crear-libro'),

    path('catalogo-libros/', views.catalogo_libros, name='catalogo_libros'),
    path('detalle_libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
]


