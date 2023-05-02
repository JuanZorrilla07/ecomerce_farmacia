
from django.urls import path

from . import views

app_name ='web'

urlpatterns = [
    path('', views.index,name='index'),
    path('producutosPorCategoria/<int:categoria_id>',views.producutosPorCategoria,name='producutosPorCategoria'),
    path('producutosPorNombre', views.producutosPorNombre, name='producutosPorNombre'),
    path('producuto/<int:producuto_id>', views.producutoDetalle, name='producuto'),
    path('carrito', views.carrito,name='carrito'),
    path('agregarCarrito/<int:producuto_id>',views.agregarCarrito,name='agregarCarrito'),
    path('eliminarProducutoCarrito/<int:producuto_id>', views.eliminarProducutoCarrito, name='eliminarProducutoCarrito'),
    path('limpiarCarrito', views.limpiarCarrito,name='limpiarCarrito')
]
