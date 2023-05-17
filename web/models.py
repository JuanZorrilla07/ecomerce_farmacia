from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nombre

class Producuto(models.Model):
    Categoria= models.ForeignKey(Categoria,on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=200)
    descripcion= models.TextField(null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen  = models.ImageField(upload_to='productos', blank=True)


    def __str__(self):
        return self.nombre

class sucursal(models.Model):
    
    
    dirrecion = models.CharField(max_length=50, )
    telefono = models.CharField(max_length=8)
    Cerro = 'Cerro'
    Sayago = 'Sayago'
    Malvin = 'Malvin'
    Centro = 'Centro'
    nombre_choice = [
        (Cerro,'Cerro'),
        (Sayago,'Sayago'),
        (Malvin,'Malvin'),
        (Centro,'Centro'),
    ]
    nombre = models.CharField(
        max_length=6,
        choices= nombre_choice,
        default= Centro,
    )
    imagen= models.ImageField(upload_to='productos', blank=True)
    link= models.CharField(max_length=300, blank=True)
    horario= models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre  

from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.RESTRICT)
    ci = models.CharField(max_length=10)
    sexo = models.CharField(max_length=1, default='M')
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(null=True)
    dirreccion = models.TextField()

    def __str__(self):
        return self.dni
 
class Pedido(models.Model):

    ESTADO_CHOICES = (
        ('0', 'Solicitado'),
        ('1','Pagado')
    )
    
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    nro_pedido = models.CharField(max_length=20,null=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    estado = models.CharField(max_length=1, default='0', choices=ESTADO_CHOICES)

    def __str__(self):
        return self.nro_pedido

class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.RESTRICT)
    Producuto = models.ForeignKey(Producuto,on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.Producuto.nombre