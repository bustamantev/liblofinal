from rest_framework import generics, status
from core.models import CategoriaLibro, Libro
from api_rest.serializers import CategoriaLibroSerializer, LibroSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.shortcuts import render

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CategoriaLibroList(generics.ListAPIView):
    queryset = CategoriaLibro.objects.all()
    serializer_class = CategoriaLibroSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class LibroList(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CrearLibro(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def catalogo_libros(request):
    next_page_url = request.GET.get('next_page_url', 'https://gutendex.com/books/')
    response = requests.get(next_page_url)
    data = response.json()
    
    libros = []
    for libro in data['results']:
        # Extraer los campos necesarios del libro
        titulo = libro['title']
        autor = libro.get('authors', [{'name': 'Desconocido'}])[0]['name']
        imagen_url = libro['formats'].get('image/jpeg', None)
        libro_id = libro['id']  # Asegúrate de obtener el ID del libro
        
        # Agregar el diccionario del libro a la lista de libros, incluyendo el ID
        libros.append({
            'id': libro_id,
            'titulo': titulo,
            'autor': autor,
            'imagen_url': imagen_url
        })

    next_page_url = data.get('next', None)
    
    # Verificar si hay una URL de página anterior disponible
    previous_page_url = data.get('previous', None)
    
    return render(request, 'core/catalogo_libros.html', {'libros': libros, 'next_page_url': next_page_url, 'previous_page_url': previous_page_url})



def detalle_libro(request, libro_id):
    # Obtener los detalles del libro desde la URL proporcionada
    url = f"https://gutendex.com/books/{libro_id}"
    response = requests.get(url)
    libro_data = response.json()

    # Extraer los campos necesarios del JSON
    titulo = libro_data.get('title')
    idiomas = libro_data.get('languages')
    autor = ', '.join([author.get('name') for author in libro_data.get('authors', [])])
    estanterias = libro_data.get('bookshelves', [])
    imagen_url = libro_data.get('formats', {}).get('image/jpeg')

    context = {
        'titulo': titulo,
        'idiomas': idiomas,
        'autor': autor,
        'estanterias': estanterias,
        'imagen_url': imagen_url,
    }

    return render(request, 'core/detalle_libro.html', context)








