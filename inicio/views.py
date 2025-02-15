from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_protect
from .models import Profile

def inicio(request):
    return render(request, 'inicio.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
    return redirect('inicio')

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        # Crear usuario
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name')
        )
        
        # Asignar al grupo de Clientes
        grupo_clientes = Group.objects.get(name='Cliente')
        user.groups.add(grupo_clientes)
        
        # Crear perfil de cliente
        Profile.objects.create(
            user=user,
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion')
        )
        
        # Iniciar sesión automáticamente
        login(request, user)
        return redirect('inicio')
    return redirect('inicio')

from rest_framework import generics
from .models import Profile, Mesa, Plato, Pedido, DetallePedido, Pago
from .serializers import ProfileSerializer, MesaSerializer, PlatoSerializer, PedidoSerializer, DetallePedidoSerializer, PagoSerializer

class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class MesaListCreateView(generics.ListCreateAPIView):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer

class MesaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer

class PlatoListCreateView(generics.ListCreateAPIView):
    queryset = Plato.objects.all()
    serializer_class = PlatoSerializer

class PlatoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plato.objects.all()
    serializer_class = PlatoSerializer

class PedidoListCreateView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PedidoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetallePedidoListCreateView(generics.ListCreateAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class DetallePedidoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer


class PagoListCreateView(generics.ListCreateAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class PagoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

