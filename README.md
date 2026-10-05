# AutoTech Management - Sistema de Gestión de Taller Mecánico

Backend desarrollado en **Django** desacoplado de almacenamiento local y conectado a una base de datos relacional en la nube (**PostgreSQL en Neon.tech**), con persistencia remota de datos en tiempo real y control de versiones en GitHub.

---

## 1. Repositorio en GitHub
- **URL:** [https://github.com/SingerVlad/autotech-backend-3](https://github.com/SingerVlad/autotech-backend-3)
- **Rama:** `main`
- **Visibilidad:** Pública

---

## 2. Requisitos Previos e Instalación

Para clonar y poner en marcha el proyecto localmente desde cero:

### 1. Clonar el repositorio
```bash
git clone https://github.com/SingerVlad/autotech-backend-3.git
cd autotech-backend-3

```
---


### 2. Crear y activar el entorno virtual
En Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

### 3. Instalar dependencias
```powershell
pip install -r requirements.txt
```

---

## 3. Conexión a Base de Datos en la Nube (Neon PostgreSQL)

El proyecto utiliza `dj-database-url` configurado en `settings.py` para conectarse a Neon PostgreSQL sin requerir base de datos local:

- **Plataforma:** [https://console.neon.tech](https://console.neon.tech)
- **Proyecto:** autotech-db
- **Cadena de Conexión:**
  ```text
  postgresql://neondb_owner:npg_7EBlnkCIXp5u@ep-blue-glitter-b43171ca-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
  ```

### Migraciones
Las migraciones ya se encuentran aplicadas en la base remota. Para verificar o sincronizar:
```powershell
python manage.py migrate
```

---

## 4. Puesta en Marcha del Servidor

```powershell
python manage.py runserver
```
Servidor disponible en: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---
## 5. Credenciales de Acceso

### Panel de Administración (Django Admin)
- **URL:** http://127.0.0.1:8000/admin/
- **Usuario Administrador:** kevin
- **Contraseña:** 123456

---

## 6. Flujo de Prueba Funcional (Paso a Paso)

### Paso A: Parametrización en el Panel de Administración (/admin/)
1. Ingrese a http://127.0.0.1:8000/admin/ con las credenciales de superusuario.
2. **Crear Marcas:** En Marcas, clic en Añadir marca (ej. Toyota, Nissan) y guarde.
3. **Crear Modelos:** En Modelos de vehículo, clic en Añadir modelo, asociar a una marca y guarde (ej. Corolla).
4. **Crear Servicios:** En Servicios, agregar el trabajo con su costo estimado (ej. Alineación y Balanceo).
5. **Usuarios:** En Usuarios se pueden gestionar roles u operadores.

### Paso B: Operación del Taller y Registro de Órdenes (/)
1. Diríjase a http://127.0.0.1:8000/.
2. Podrá visualizar la tabla con las Órdenes de Trabajo Activas.
3. Haga clic en "Registrar Nueva Orden" (o "+ Nueva Orden").
4. Complete los datos (Patente, Marca, Modelo, Cliente, Servicio y Costo).
5. Presione Guardar: la orden se registrará de inmediato y se almacenará en Neon PostgreSQL.

---

## 7. Inspección de Datos en Neon Console
1. Inicie sesión en https://console.neon.tech y acceda al proyecto autotech-db.
2. En el menú lateral seleccione Tables (esquema public).
3. En las tablas taller_ordentrabajo, taller_vehiculo y taller_marca se apreciarán los registros en tiempo real.

## 🚀 API RESTful - Documentación y Arquitectura (Evaluación Unidad 3)

### 1. Arquitectura y Mecanismo de Autenticación
- **Framework:** Django REST Framework (DRF).
- **Esquema de Autenticación:** Se implementó `TokenAuthentication` junto con `SessionAuthentication`.
  - **Justificación Técnica:** La autenticación basada en Tokens (`rest_framework.authtoken`) desacopla el backend del cliente, permitiendo el consumo seguro de recursos por parte de aplicaciones móviles, SPAs (React, Vue) o microservicios externos mediante el encabezado HTTP estándar:
    ```http
    Authorization: Token <tu_token_aqui>
    ```
- **Control de Acceso y Permisos:** Se configuró la política global `IsAuthenticatedOrReadOnly`.
  - **Consultas anónimas (`GET`):** Abiertas al público para consultar catálogo de servicios y fichas.
  - **Mutaciones (`POST`, `PUT`, `PATCH`, `DELETE`):** Requieren obligatoriamente credenciales válidas o token activo, devolviendo `401 Unauthorized` o `403 Forbidden` en caso contrario.

### 2. Catálogo de Endpoints RESTful

| Recurso | Método HTTP | Endpoint | Descripción | Código Éxito |
| :--- | :---: | :--- | :--- | :---: |
| **Servicios** | `GET` | `/api/servicios/` | Listado completo de servicios | `200 OK` |
| | `POST` | `/api/servicios/` | Registro de nuevo servicio técnico | `201 Created` |
| | `GET` | `/api/servicios/<id>/` | Detalle específico de un servicio | `200 OK` |
| | `PUT` / `PATCH` | `/api/servicios/<id>/` | Actualización total o parcial | `200 OK` |
| | `DELETE` | `/api/servicios/<id>/` | Eliminación de servicio | `204 No Content` |
| **Vehículos** | `GET` / `POST` | `/api/vehiculos/` | Listar y dar de alta vehículos | `200` / `201` |
| | `GET` / `PUT` / `DELETE`| `/api/vehiculos/<id>/` | Operaciones puntuales por patente/ID | `200` / `204` |
| **Órdenes de Trabajo**| `GET` / `POST` | `/api/ordenes/` | Listar y crear órdenes de trabajo | `200` / `201` |
| | `GET` / `PUT` / `DELETE`| `/api/ordenes/<id>/` | Detalle, avance de estado y costos | `200` / `204` |
| **Autenticación** | `POST` | `/api/api-token-auth/` | Obtención de Token con credenciales | `200 OK` |

### 3. Códigos de Estado Implementados
- `200 OK`: Peticiones de lectura y actualización exitosas.
- `201 Created`: Creación exitosa de recursos vía `POST`.
- `204 No Content`: Eliminación confirmada sin cuerpo de retorno (`DELETE`).
- `400 Bad Request`: Error de validación en la estructura del JSON enviado.
- `401 Unauthorized` / `403 Forbidden`: Acceso no autorizado o token ausente.
- `404 Not Found`: Recurso no encontrado.

