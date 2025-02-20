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

    path('api/platos/', views.PlatoListView.as_view(), name='plato-list'),
    path('api/categorias/', views.CategoriaListView.as_view(), name='categoria-list'),
    path('api/detallepedidos/', views.DetallePedidoCreateView.as_view(), name='detallepedido-create'),
    path('api/pedidos/', views.PedidoCreateView.as_view(), name='pedido-create'),
    path('api/pagos/', views.PagoCreateView.as_view(), name='pago-create'),

    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)