from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_protect
from .models import Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

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
            direccion=request.POST.get('direccion'),
            cedula=request.POST.get('cedula')
        )
        
        # Iniciar sesión automáticamente
        login(request, user)
        return redirect('inicio')
    return redirect('inicio')

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import Categoria, Plato, Pedido, DetallePedido, Pago
from .serializers import UserSerializer, CategoriaSerializer, PlatoSerializer, PedidoSerializer, DetallePedidoSerializer, PagoSerializer
from rest_framework.authtoken.models import Token


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Añadir el usuario al grupo "Cliente"
            grupo_clientes = Group.objects.get(name='Cliente')
            user.groups.add(grupo_clientes)
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class PlatoDetailView(generics.RetrieveAPIView):
    queryset = Plato.objects.all()
    serializer_class = PlatoSerializer
    permission_classes = [permissions.AllowAny]

class PlatoListView(generics.ListAPIView):
    queryset = Plato.objects.all()
    serializer_class = PlatoSerializer
    permission_classes = [permissions.AllowAny]

class CategoriaDetailView(generics.RetrieveAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]

class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]

class DetallePedidoCreateView(generics.CreateAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PedidoCreateView(generics.CreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class PagoCreateView(generics.CreateAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [permissions.IsAuthenticated]