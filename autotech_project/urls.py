from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from taller import views

urlpatterns = [
    # Panel de administración y rutas web existentes
    path('admin/', admin.site.urls),
    path('', include('taller.urls')),

    # --- ENDPOINTS API RESTful (Unidad 3) ---
    # Autenticación: Endpoint para obtener token vía POST con username y password
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # Permite iniciar/cerrar sesión en la interfaz web de DRF
    path('api-auth/', include('rest_framework.urls')),

    # Endpoints de Servicios
    path('api/servicios/', views.ServicioListCreateAPIView.as_view(), name='api_servicio_list'),
    path('api/servicios/<int:pk>/', views.ServicioDetailAPIView.as_view(), name='api_servicio_detail'),

    # Endpoints de Vehículos
    path('api/vehiculos/', views.VehiculoListCreateAPIView.as_view(), name='api_vehiculo_list'),
    path('api/vehiculos/<int:pk>/', views.VehiculoDetailAPIView.as_view(), name='api_vehiculo_detail'),

    # Endpoints de Órdenes de Trabajo
    path('api/ordenes/', views.OrdenTrabajoListCreateAPIView.as_view(), name='api_orden_list'),
    path('api/ordenes/<int:pk>/', views.OrdenTrabajoDetailAPIView.as_view(), name='api_orden_detail'),
]