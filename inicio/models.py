from django.db import models
from django.contrib.auth.models import User  # Usuario por defecto de Django
from django.db.models import Sum
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación 1 a 1 con User
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Mesa(models.Model):
    ESTADO_MESA = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
    ]

    numero_mesa = models.IntegerField(unique=True)
    estado_mesa = models.CharField(max_length=40, choices=ESTADO_MESA, default='disponible')

    def __str__(self):
        return f"Mesa {self.numero_mesa}"

class Plato(models.Model):
    ESTADO_PLATO = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No Disponible'),
    ]

    nombre_plato = models.CharField(max_length=150)
    descripcion = models.TextField()
    img_plato = models.ImageField(upload_to='img_plato/', blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_PLATO, default='disponible')
    tiempo = models.IntegerField(help_text="Tiempo de cocción en minutos")

    def __str__(self):
        return self.nombre_plato

    def delete(self, *args, **kwargs):
        if self.img_plato:
            if os.path.isfile(self.img_plato.path):
                os.remove(self.img_plato.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            this = Plato.objects.get(id=self.id)
            if this.img_plato != self.img_plato:
                this.img_plato.delete(save=False)
        except Plato.DoesNotExist:
            pass
        super().save(*args, **kwargs)

class Pedido(models.Model):
    ESTADO_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
        ('en camino', 'En Camino'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario de Django
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default='pendiente')

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.precio_total = self.plato.precio * self.cantidad
        super().save(*args, **kwargs)

class Pago(models.Model):
    METODO_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
    ]

    ESTADO_PAGO = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO, default='efectivo')
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO, default='pendiente')
    comprobante_pago = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.monto_total = sum(detalle.precio_total for detalle in self.pedido.detallepedido_set.all())
        try:
            this = Pago.objects.get(id=self.id)
            if this.comprobante_pago != self.comprobante_pago:
                this.comprobante_pago.delete(save=False)
        except Pago.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.comprobante_pago:
            if os.path.isfile(self.comprobante_pago.path):
                os.remove(self.comprobante_pago.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Pago {self.id} - Pedido {self.pedido.id}"