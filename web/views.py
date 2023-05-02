from django.shortcuts import get_object_or_404, render, redirect

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


"""vistas para el carrito de compras"""
from .carrito import Cart

def carrito(request):
    return render(request, 'carrito.html')

def agregarCarrito(request,producuto_id):
    if request.method == 'POST':
       cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1    

    objProducuto = Producuto.objects.get(pk=producuto_id)
    carritoProducuto = Cart(request)
    carritoProducuto.add(objProducuto,cantidad)

    if request.method == 'GET':
        return redirect('/')

    
    return render(request,'carrito.html')
    

def eliminarProducutoCarrito(request,producuto_id):
    objPorducuto = Producuto.objects.get(pk=producuto_id)
    carritoProducuto = Cart(request)
    carritoProducuto.delete(objPorducuto)

    return render(request,'carrito.html')

def limpiarCarrito(request):
    carritoProducuto = Cart(request)
    carritoProducuto.clear()

    return render(request,'carrito.html')