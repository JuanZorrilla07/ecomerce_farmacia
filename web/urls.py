
from django.urls import path

from . import views

app_name ='web'

urlpatterns = [
    path('', views.index,name='index'),
    path('producutosPorCategoria/<int:categoria_id>',views.producutosPorCategoria,name='producutosPorCategoria'),
    path('producutosPorNombre', views.producutosPorNombre, name='producutosPorNombre'),
    path('producuto/<int:producuto_id>', views.producutoDetalle, name='producuto')
]
