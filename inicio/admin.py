from django.contrib import admin
from .models import Mesa, Plato, Pedido, DetallePedido, Pago, Categoria, Profile
from django.utils.html import format_html
from django.contrib.admin.widgets import AutocompleteSelect
import mimetypes
# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    list_per_page = 10

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'direccion', 'cedula')
    list_per_page = 10

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ('nombre_plato', 'categoria', 'mostar_img', 'precio', 'estado', 'tiempo')
    list_filter = ('estado', 'precio')
    search_fields = ('nombre_plato', 'descripcion')
    list_editable = ('estado',)
    list_per_page = 10
    def mostar_img(self, obj):
        if obj.img_plato:  
            return format_html('<img src="{}" style="width: 100px; height: 80px;" />', obj.img_plato.url)
        return "Sin Imagen"
    mostar_img.short_description = "Imagen" 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "plato":
            kwargs["widget"] = AutocompleteSelect(db_field.remote_field, self.admin_site)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_entrega', 'mesa', 'estado')
    list_filter = ('estado', 'fecha_entrega')
    search_fields = ('usuario__username', 'mesa__numero_mesa')
    list_editable = ('estado', 'fecha_entrega')
    list_per_page = 10




@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido','plato', 'cantidad', 'precio_total')
    readonly_fields = ('precio_total',)
    list_editable = ('cantidad',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'monto_total', 'metodo_pago', 'estado_pago', 'mostrar_comprobante', 'fecha_pago')
    readonly_fields = ('monto_total', 'mostrar_comprobante')
    list_editable = ('estado_pago', 'metodo_pago')
    list_filter = ('estado_pago', 'metodo_pago', 'fecha_pago')

    def mostrar_comprobante(self, obj):
        if obj.comprobante_pago:
            file_url = obj.comprobante_pago.url
            file_type, _ = mimetypes.guess_type(file_url)

            if file_type and file_type.startswith('image'):
                # Si es una imagen, mostrar una miniatura
                return format_html('<img src="{}" style="width: 100px; height: auto; border-radius: 5px;" />', file_url)
            elif file_type == 'application/pdf':
                # Si es un PDF, mostrar un enlace de previsualización
                return format_html('<a href="{}" target="_blank">Ver PDF</a>', file_url)

        return "Sin Comprobante"

    mostrar_comprobante.short_description = "Comprobante de Pago"

    autocomplete_fields = ['pedido'] 
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "pedido":
            if request.resolver_match.kwargs.get('object_id'):
                pago_id = request.resolver_match.kwargs.get('object_id')
                pago = Pago.objects.get(id=pago_id)
                kwargs["queryset"] = Pedido.objects.exclude(id__in=Pago.objects.exclude(id=pago_id).values_list('pedido_id', flat=True))
            else:
                kwargs["queryset"] = Pedido.objects.exclude(id__in=Pago.objects.values_list('pedido_id', flat=True))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero_mesa',  'estado_mesa')
    list_editable = ('estado_mesa',)
    list_per_page = 10



 