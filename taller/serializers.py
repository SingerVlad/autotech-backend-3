from rest_framework import serializers
from .models import Marca, ModeloVehiculo, Vehiculo, Servicio, OrdenTrabajo


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre']


class ModeloVehiculoSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.ReadOnlyField(source='marca.nombre')

    class Meta:
        model = ModeloVehiculo
        fields = ['id', 'marca', 'marca_nombre', 'nombre']


class VehiculoSerializer(serializers.ModelSerializer):
    modelo_nombre = serializers.ReadOnlyField(source='modelo_referencia.nombre')
    marca_nombre = serializers.ReadOnlyField(source='modelo_referencia.marca.nombre')

    class Meta:
        model = Vehiculo
        fields = [
            'id',
            'patente',
            'modelo_referencia',
            'marca_nombre',
            'modelo_nombre',
            'anio',
            'cliente_nombre',
            'cliente_telefono',
        ]


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'precio_base']


class OrdenTrabajoSerializer(serializers.ModelSerializer):
    vehiculo_patente = serializers.ReadOnlyField(source='vehiculo.patente')
    servicio_nombre = serializers.ReadOnlyField(source='servicio.nombre')
    estado_display = serializers.ReadOnlyField(source='get_estado_display')
    costo_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrdenTrabajo
        fields = [
            'id',
            'vehiculo',
            'vehiculo_patente',
            'servicio',
            'servicio_nombre',
            'fecha_ingreso',
            'fecha_entrega_estimada',
            'estado',
            'estado_display',
            'costo_repuestos',
            'costo_total',
            'observaciones',
        ]