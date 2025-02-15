from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', views.ProfileRetrieveUpdateDestroyView.as_view(), name='profile-detail-update-destroy'),
    
    path('mesas/', views.MesaListCreateView.as_view(), name='mesa-list-create'),
    path('mesas/<int:pk>/', views.MesaRetrieveUpdateDestroyView.as_view(), name='mesa-detail-update-destroy'),
    
    path('platos/', views.PlatoListCreateView.as_view(), name='plato-list-create'),
    path('platos/<int:pk>/', views.PlatoRetrieveUpdateDestroyView.as_view(), name='plato-detail-update-destroy'),
    
    path('pedidos/', views.PedidoListCreateView.as_view(), name='pedido-list-create'),
    path('pedidos/<int:pk>/', views.PedidoRetrieveUpdateDestroyView.as_view(), name='pedido-detail-update-destroy'),
    
    path('detalle-pedidos/', views.DetallePedidoListCreateView.as_view(), name='detalle-pedido-list-create'),
    path('detalle-pedidos/<int:pk>/', views.DetallePedidoRetrieveUpdateDestroyView.as_view(), name='detalle-pedido-detail-update-destroy'),
    
    path('reservas-mesas/', views.ReservaMesaListCreateView.as_view(), name='reserva-mesa-list-create'),
    path('reservas-mesas/<int:pk>/', views.ReservaMesaRetrieveUpdateDestroyView.as_view(), name='reserva-mesa-detail-update-destroy'),
    
    path('pagos/', views.PagoListCreateView.as_view(), name='pago-list-create'),
    path('pagos/<int:pk>/', views.PagoRetrieveUpdateDestroyView.as_view(), name='pago-detail-update-destroy'),
]
