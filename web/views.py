from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Categoria, Producuto, Cliente, Pedido, PedidoDetalle
from paypal.standard.forms import PayPalPaymentsForm

from django.urls import reverse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


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

"""vistas para clientes y usarios"""

from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

from .forms import ClienteForm


def crearUsuario(request):

    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        nuevoUsuario = User.objects.create_user(username=dataUsuario,password=dataPassword)
        if nuevoUsuario is not None:
            login(request,nuevoUsuario)
            return redirect('/cuenta')


    return render(request,'login.html')

def loginUsuario(request):
    paginaDestino = request.GET.get('next',None)
    context = {
        'destino':paginaDestino
    }

    if request.method =='POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']

        usuarioAuth = authenticate(request,username=dataUsuario,password=dataPassword)
        if usuarioAuth is not None:
            login(request,usuarioAuth)

            if dataDestino != 'None':
                return redirect(dataDestino)

            return redirect('/cuenta')
        else:
            context = {
                'mensajeError':'Datos incorrecros'
            }


    return render(request,'login.html',context)

def logoutUsuario(request):
    logout(request)
    return render(request,'login.html') 

def cuentaUsuario(request):

    try:
        clienteEditar = Cliente.objects.get(usuario = request.user)

        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'dirrecion':clienteEditar.dirreccion,
            'telefono':clienteEditar.telefono,
            'ci':clienteEditar.ci,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento
        }
    except:   
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
        }

    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente':frmCliente
    }

    return render(request,'cuenta.html',context)

def actualizarCliente(request):
    mensaje = ''

    if request.method == 'POST':
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data

            #actualizar usario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = dataCliente['nombre']
            actUsuario.last_name = dataCliente['apellidos']
            actUsuario.email = dataCliente['email']
            actUsuario.save()


            #registar cliente
            nuevoCliente = Cliente()
            nuevoCliente.usuario = actUsuario
            nuevoCliente.ci = dataCliente['ci']
            nuevoCliente.dirreccion = dataCliente['direccion']
            nuevoCliente.telefono = dataCliente['telefono']
            nuevoCliente.sexo = dataCliente['sexo']
            nuevoCliente.fecha_nacimiento = dataCliente['fecha_nacimiento']
            nuevoCliente.save()

            mensaje = 'Datos actualizados'
    
    context = {
        'mensaje':mensaje,
        'frmCliente':frmCliente
    }
    
    return render(request,'cuenta.html',context)     


"""Vistas para proceso de compras"""


@login_required(login_url='/login')
def registrarPedido(request):
    try:
        clienteEditar = Cliente.objects.get(usuario = request.user)

        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'dirrecion':clienteEditar.dirreccion,
            'telefono':clienteEditar.telefono,
            'ci':clienteEditar.ci,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento
        }
    except:   
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
        }

    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente':frmCliente
    }
 

    return render(request,'pedido.html',context)

@login_required(login_url='/login')
def confirmarPedido(request):
    context = {}
    if request.method == "POST":
        #actualizar datos de usarios
        actUsuario = User.objects.get(pk=request.user.id)
        actUsuario.first_name = request.POST['nombre']
        actUsuario.last_name = request.POST['apellidos']
        actUsuario.save()
        #registrmaos o actualizamos datos del cliente
        try:
            clientePedido = Cliente.objects.get(usuario=request.user)
            clientePedido.telefono = request.POST['telefono']
            clientePedido.dirreccion = request.POST['direccion']
            clientePedido.save()
        except:
            clientePedido = Cliente()
            clientePedido.usuario = actUsuario
            clientePedido.dirreccion = request.POST['direccion']
            clientePedido.telefono = request.POST['telefono']
            clientePedido.save() 
        #registramos pedido
        nroPedido = ''
        montoTotal = float(request.session.get('cartMontoTotal'))
        nuevoPedido = Pedido()
        nuevoPedido.cliente = clientePedido
        nuevoPedido.save()

        #registramos el detalle del pedido
        carritoPedido = request.session.get('cart')
        for key,value in carritoPedido.items():
            
            producutoPedido = Producuto.objects.get(pk=value['producuto_id'])
            Detalle = PedidoDetalle()
            Detalle.pedido = nuevoPedido
            Detalle.producuto = producutoPedido
            Detalle.cantidad = int(value['cantidad'])
            Detalle.subtotal = float(value['subtotal'])
            Detalle.save()
            montoTotal += float(value['subtotal'])
           
            #creamos boton Paypal


        #actualzar pedido
        nroPedido = 'PED'+ nuevoPedido.fecha_registro.strftime('%Y') + str(nuevoPedido.id)
        nuevoPedido.nro_pedido = nroPedido
        nuevoPedido.monto_total = montoTotal
        nuevoPedido.save()
        
        #registrar variable de sesion para rel pedido 
        request.session['pedidoId'] = nuevoPedido.id

        #boton de paypal 
        paypal_dict = {
        "business":     "sb-mvtyu25103667@business.example.com",
        "amount": montoTotal,
        "item_name": "PEDIDO CODIGO :" + nroPedido, 
        "invoice": "100-ED100",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('/'),
        "cancel_return": request.build_absolute_uri('/logout'),
    }

    # Create the instance.
    formPaypal = PayPalPaymentsForm(initial=paypal_dict)


    context = {
            'pedido':nuevoPedido,
            'formPaypal':formPaypal
        }

    #limpiar carrito de comrpas
    carrito = Cart(request)
    carrito.clear()

    return render(request, 'compra.html', context)

@login_required(login_url='/login')
def gracias(request):
    paypalId = request.GET.get('PayerID',None)
    context = {}
    if paypalId is not None:
        pedidoId = request.session.get('pedidoId')
        pedido = Pedido.objects.get(pk=pedidoId)
        pedido.estado = '1'
        pedido.save()

        send_mail(
                "GRACIAS POR TU COMPRA",
                "Tu nro de pedido es " + pedido.nro_pedido,
                settings.ADMIN_USER_EMAIL,
                ["request.user.email,"],
                fail_silently=False,
            )

        context = {
            'pedido':pedido
        }
    else:
       return redirect('/')  
    return render (request,'gracias.html',context)



        #CREAMOS EL BOTON DE PAYPAL
 

def confirmacionPedido(request):
    return render(request,'gracias.html')