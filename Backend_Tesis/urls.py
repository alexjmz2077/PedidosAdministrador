"""
URL configuration for Backend_Tesis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from inicio import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),

    path('api/token/', obtain_auth_token, name='api_token_auth'),

    path('api/profiles/', views.ProfileListCreateView.as_view(), name='profile-list-create'),
    path('api/profiles/<int:pk>/', views.ProfileRetrieveUpdateDestroyView.as_view(), name='profile-detail'),
    path('api/mesas/', views.MesaListCreateView.as_view(), name='mesa-list-create'),
    path('api/mesas/<int:pk>/', views.MesaRetrieveUpdateDestroyView.as_view(), name='mesa-detail'),
    path('api/platos/', views.PlatoListCreateView.as_view(), name='plato-list-create'),
    path('api/platos/<int:pk>/', views.PlatoRetrieveUpdateDestroyView.as_view(), name='plato-detail'),
    path('api/pedidos/', views.PedidoListCreateView.as_view(), name='pedido-list-create'),
    path('api/pedidos/<int:pk>/', views.PedidoRetrieveUpdateDestroyView.as_view(), name='pedido-detail'),
    path('api/detallepedidos/', views.DetallePedidoListCreateView.as_view(), name='detallepedido-list-create'),
    path('api/detallepedidos/<int:pk>/', views.DetallePedidoRetrieveUpdateDestroyView.as_view(), name='detallepedido-detail'),
    path('api/pagos/', views.PagoListCreateView.as_view(), name='pago-list-create'),
    path('api/pagos/<int:pk>/', views.PagoRetrieveUpdateDestroyView.as_view(), name='pago-detail'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)