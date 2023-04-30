from django.shortcuts import get_object_or_404, render

from .models import Categoria, Producuto

# Create your views here.
"""vistas  para el catalogo"""

def index(request):
    listaProducutos = Producuto.objects.all()
    listaCategorias = Categoria.objects.all()
    
    print(listaProducutos)
    context = {
        'producutos':listaProducutos,
        'categorias':listaCategorias
    }
    return render(request,'index.html',context)

def producutosPorCategoria(request,categoria_id):
    """vista para filtrar categorias"""
    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaProducutos = objCategoria.producuto_set.all()

    listaCategorias = Categoria.objects.all()

    context = {
        'categorias':listaCategorias,
        'producutos':listaProducutos

    }
    return render(request,'index.html',context)

def producutosPorNombre(request):
    nombre= request.POST['nombre']

    listaProducutos = Producuto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()

    context = {
        'categorias':listaCategorias,
        'producutos':listaProducutos

    }
    return render(request,'index.html', context)

def producutoDetalle(request,producuto_id):
    """vista para el detalle dl producto"""

    #objProducuto = Producuto.objects.get(pk=producuto_id)
    objProducuto = get_object_or_404(Producuto,pk=producuto_id)
    context = {
        'producuto':objProducuto
    }
    return render(request,'producto.html',context)