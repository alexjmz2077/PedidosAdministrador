from rest_framework import serializers
from .models import Profile, Mesa, Plato, Pedido, DetallePedido, Pago, Categoria
from django.contrib.auth.models import User
from datetime import datetime

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['telefono', 'direccion', 'cedula']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        Profile.objects.create(
            user=user,
            telefono=profile_data['telefono'],
            direccion=profile_data['direccion'],
            cedula=profile_data['cedula']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class PlatoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()

    class Meta:
        model = Plato
        fields = ['id', 'nombre_plato', 'descripcion', 'img_plato', 'precio', 'estado', 'tiempo', 'categoria']


class PedidoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['mesa']  # Solo incluir el campo 'mesa' para el método POST

    def create(self, validated_data):
        mesa = validated_data['mesa']
        
        validated_data['usuario'] = self.context['request'].user
        validated_data['estado'] = 'pendiente'
        validated_data['fecha_entrega'] = datetime.now()
        #if mesa.estado_mesa == 'ocupada':
        #    raise serializers.ValidationError('Ocupada')
        #mesa.estado_mesa = 'ocupada'
        #mesa.save()
        return super().create(validated_data)

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'fecha_entrega', 'mesa', 'estado'] 

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = ['cantidad', 'pedido', 'plato', 'precio_total']
        read_only_fields = ['precio_total']

    def validate_pedido(self, value):
        if value.usuario != self.context['request'].user:
            raise serializers.ValidationError("El pedido no pertenece al usuario autenticado.")
        return value

    def create(self, validated_data):
        detalle_pedido = DetallePedido(**validated_data)
        detalle_pedido.precio_total = detalle_pedido.cantidad * detalle_pedido.plato.precio
        detalle_pedido.save()
        return detalle_pedido

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'