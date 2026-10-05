from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Marca, ModeloVehiculo, Vehiculo, Servicio, OrdenTrabajo
from .forms import OrdenTrabajoCompletaForm
from .serializers import (
    MarcaSerializer,
    ModeloVehiculoSerializer,
    VehiculoSerializer,
    ServicioSerializer,
    OrdenTrabajoSerializer,
)


# ==========================================
# 1. VISTAS WEB TRADICIONALES (HTML / Plantillas)
# ==========================================

def lista_ordenes(request):
    ordenes = OrdenTrabajo.objects.select_related(
        'vehiculo__modelo_referencia__marca', 
        'servicio'
    ).all().order_by('-fecha_ingreso')
    return render(request, 'taller/lista_ordenes.html', {'ordenes': ordenes})


def detalle_orden(request, pk):
    orden = get_object_or_404(
        OrdenTrabajo.objects.select_related('vehiculo__modelo_referencia__marca', 'servicio'), 
        pk=pk
    )
    return render(request, 'taller/detalle_orden.html', {'orden': orden})


def crear_orden(request):
    if request.method == 'POST':
        form = OrdenTrabajoCompletaForm(request.POST)
        if form.is_valid():
            orden = form.save()
            messages.success(request, f"Orden #{orden.id} creada exitosamente para el vehículo {orden.vehiculo.patente}.")
            return redirect('taller:lista_ordenes')
    else:
        form = OrdenTrabajoCompletaForm()

    return render(request, 'taller/formulario_orden.html', {'form': form})


def obtener_modelos_por_marca(request):
    marca_id = request.GET.get('marca_id')
    modelos = ModeloVehiculo.objects.filter(marca_id=marca_id).values('id', 'nombre').order_by('nombre')
    return JsonResponse(list(modelos), safe=False)


# ==========================================
# 2. VISTAS API RESTful (Django REST Framework)
# ==========================================

# --- SERVICIOS ---
class ServicioListCreateAPIView(generics.ListCreateAPIView):
    """GET: Lista todos los servicios. POST: Registra un nuevo servicio."""
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ServicioDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET: Detalle de servicio. PUT/PATCH: Actualizar. DELETE: Eliminar."""
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# --- VEHÍCULOS ---
class VehiculoListCreateAPIView(generics.ListCreateAPIView):
    """GET: Lista vehículos registrados. POST: Registra un nuevo vehículo."""
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VehiculoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET: Detalle de vehículo. PUT/PATCH: Modificar datos. DELETE: Eliminar."""
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# --- ÓRDENES DE TRABAJO ---
class OrdenTrabajoListCreateAPIView(generics.ListCreateAPIView):
    """GET: Lista órdenes de trabajo. POST: Crea una nueva orden."""
    queryset = OrdenTrabajo.objects.all()
    serializer_class = OrdenTrabajoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OrdenTrabajoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET: Detalle de orden. PUT/PATCH: Actualizar estado o costos. DELETE: Eliminar."""
    queryset = OrdenTrabajo.objects.all()
    serializer_class = OrdenTrabajoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]