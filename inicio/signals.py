from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DetallePedido, Pago

@receiver(post_save, sender=DetallePedido)
@receiver(post_delete, sender=DetallePedido)
def actualizar_monto_total(sender, instance, **kwargs):
    pedido = instance.pedido
    pagos = Pago.objects.filter(pedido=pedido)
    for pago in pagos:
        pago.monto_total = sum(detalle.precio_total for detalle in pedido.detallepedido_set.all())
        pago.save()