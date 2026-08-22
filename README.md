# Help Desk & Smart Inventory — Backend

Backend de la plataforma **Help Desk & Smart Inventory**, desarrollado con **Django** y **Django REST Framework**. El sistema proporciona una API REST centralizada para la gestión de tickets de soporte, inventario tecnológico, usuarios, dispositivos y asistencia mediante inteligencia artificial.

El backend funciona como núcleo de comunicación entre la aplicación cliente, la base de datos y los servicios externos utilizados por la plataforma.

---

## Descripción

El backend proporciona los servicios necesarios para administrar una plataforma de soporte técnico orientada a organizaciones que necesitan centralizar sus incidencias, controlar sus activos tecnológicos y ofrecer asistencia automatizada.

Entre sus principales responsabilidades se encuentran:

* Gestión de usuarios y permisos.
* Administración de tickets de soporte.
* Gestión de activos tecnológicos.
* Registro y seguimiento de dispositivos.
* Gestión de incidencias y estados.
* Exposición de API REST para clientes externos.
* Integración con servicios de inteligencia artificial.
* Procesamiento de conversaciones del asistente de soporte.
* Persistencia de información mediante PostgreSQL.
* Comunicación con Supabase.
* Configuración mediante variables de entorno.
* Ejecución mediante contenedores Docker.

---

## Características principales

### Help Desk

Permite administrar el ciclo de vida de las solicitudes de soporte:

* Creación de tickets.
* Asignación de responsables.
* Estados de atención.
* Prioridades.
* Categorías.
* Seguimiento de incidencias.
* Historial de cambios.
* Registro de información relacionada con el ticket.

### Inventario inteligente

Centraliza la información de los activos tecnológicos de la organización:

* Computadoras.
* Dispositivos.
* Componentes.
* Información de hardware.
* Información de software.
* Usuarios asociados.
* Estado del activo.
* Identificadores y datos técnicos.
* Historial de información del dispositivo.

### Asistente de soporte con IA

El backend integra la API de **Google Gemini** para proporcionar funcionalidades de asistencia mediante inteligencia artificial.

El servicio permite procesar consultas de soporte y generar respuestas asistidas utilizando información contextual proporcionada por la plataforma.

Flujo simplificado:

Usuario
   │
   ▼
Angular / Electron
   │
   │ HTTP REST
   ▼
Django REST API
   │
   ├──────────────► Base de datos
   │
   └──────────────► Gemini API
                         │
                         ▼
                    Respuesta IA
                         │
                         ▼
                    Cliente

La integración con Gemini se mantiene encapsulada dentro del backend para evitar exponer credenciales o lógica sensible directamente en el cliente.

---

## Arquitectura

La solución utiliza una arquitectura basada en API REST:

    [Angular Frontend Frontend] - [Electron Desktop App] ────► [Windows Service] 
                            │                                          │
                            ├──────────────────────────────────────────│                                      
                            ▼                                          
                      [HTTP / REST]                                    
                            │                                           
                            ▼
                    [Django REST API] ────► [Gemini API]
                            │
                            ▼ 
                 [PostgreSQL / Supabase] 

### Componentes

| Componente              | Responsabilidad                                          |
| ----------------------- | -------------------------------------------------------- |
| Django                  | Framework principal del backend                          |
| Django REST Framework   | Exposición de servicios REST                             |
| PostgreSQL              | Persistencia de datos                                    |
| Supabase                | Infraestructura y servicios relacionados con PostgreSQL  |
| Docker                  | Contenerización del backend                              |
| Gemini API              | Asistencia mediante IA                                   |
| Angular                 | Cliente web                                              |
| Electron                | Aplicación de escritorio                                 |
| Node.js Windows Service | Servicio local para interacción con el sistema operativo |

---

## Stack tecnológico

| Tecnología            | Uso                             |
| --------------------- | ------------------------------- |
| Python                | Lenguaje principal              |
| Django                | Framework backend               |
| Django REST Framework | API REST                        |
| PostgreSQL            | Base de datos                   |
| Supabase              | Plataforma de datos             |
| Docker                | Contenedores                    |
| Google Gemini API     | Inteligencia artificial         |
| REST                  | Comunicación entre aplicaciones |
| Git                   | Control de versiones            |

---

## Estructura del proyecto

> Esta es la estructura del proyecto.

backend/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── ai_support/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── urls.py
│   ├── views
│
├── asset/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── signals.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│
├── report/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│
├── ticket/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── signals.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│
├── user/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── email_service.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│
├── requirements/
│
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env
├── .gitattributes
├── .gitignore
└── README.md

La aplicación está organizada por dominios funcionales para facilitar el mantenimiento y evolución del sistema.

---

## API REST

El backend expone una API REST consumida principalmente por:

* Aplicación Angular.
* Aplicación de escritorio basada en Electron.
* Otros clientes autorizados.

## Endpoints de la API

Autenticación

Método	  Endpoint	                        Descripción	 

POST	  /token	                        Obtiene un par de tokens
POST	  /token/refresh/	                Renueva el access token
POST	  /auth/login/	                    Inicio de sesión
POST	  /auth/logout/	                    Cierre de sesión e invalidación del token
POST	  /auth/refresh/	                Renueva el token de acceso
GET	      /auth/user/	                    Obtiene información del usuario autenticado
POST	  /auth/request-password-reset/	    Solicita recuperación de contraseña
POST	  /auth/reset-password/	            Restablece la contraseña
POST	  /auth/change-password/	        Cambia la contraseña del usuario
POST	  /auth/activate-account/	        Activa una cuenta de usuario

-- Usuarios y departamentos

Estas rutas son generadas mediante DefaultRouter.

Método	 Endpoint	          Descripción

GET	     /users/	          Lista usuarios
POST	 /users/	          Crea un usuario
GET	     /users/{id}/	      Obtiene un usuario
PUT	     /users/{id}/	      Actualiza un usuario
PATCH	 /users/{id}/	      Actualiza parcialmente un usuario
DELETE	 /users/{id}/	      Elimina un usuario
GET	     /departments/	      Lista departamentos
POST	 /departments/	      Crea un departamento
GET	     /departments/{id}/	  Obtiene un departamento
PUT	     /departments/{id}/	  Actualiza un departamento
PATCH	 /departments/{id}/	  Actualiza parcialmente un departamento
DELETE	 /departments/{id}/	  Elimina un departamento

-- Inventario / Assets

El AssetViewSet genera automáticamente las operaciones CRUD mediante DefaultRouter.

Método	      Endpoint	                     Descripción

GET	        /inventory/	                     Lista los activos registrados
POST	    /inventory/	                     Registra un nuevo activo
GET	        /inventory/{id}/	             Obtiene el detalle de un activo
PUT	        /inventory/{id}/	             Actualiza un activo
PATCH	    /inventory/{id}/	             Actualiza parcialmente un activo
DELETE	    /inventory/{id}/	             Elimina un activo
POST	    /assets/agent/register/	         Registra un activo mediante el agente recolector
PUT/PATCH	/assets/agent/update/{serial}/	 Actualiza información de un activo mediante su número de serie
GET	        /assets/agent/{serial}/	         Consulta un activo mediante su número de serie

-- Help Desk / Tickets

El TicketViewSet genera las operaciones CRUD:

Método	Endpoint	    Descripción

GET	    /tickets/	    Lista tickets
POST	/tickets/	    Crea un ticket
GET	    /tickets/{id}/	Obtiene el detalle de un ticket
PUT	    /tickets/{id}/	Actualiza un ticket
PATCH	/tickets/{id}/	Actualiza parcialmente un ticket
DELETE	/tickets/{id}/	Elimina un ticket

-- Asistente de soporte con IA

Método	Endpoint	                        Descripción

POST	/support-ai/chat/	                Envía un mensaje al asistente de IA
GET	    /support-ai/sessions/	            Lista las sesiones de soporte
GET	    /support-ai/sessions/{id}/	        Obtiene el detalle de una sesión
POST	/support-ai/{session_id}/escalate/	Escala una sesión de IA a soporte humano
POST	/support-ai/{session_id}/solved/	Marca una sesión como resuelta

-- Reportes y Dashboard

Método	Endpoint	                   Descripción
GET	    /reports/dashboard/	           Obtiene información general para el dashboard
GET	    /reports/tickets-status/	   Reporte de tickets agrupados por estado
GET	    /reports/tickets-category/	   Reporte de tickets agrupados por categoría
GET	    /reports/tickets-priority/	   Reporte de tickets agrupados por prioridad
GET	    /reports/tickets-technician/   Reporte de tickets por técnico
GET	    /reports/tickets-department/   Reporte de tickets por departamento
GET	    /reports/tickets-month/	       Reporte de tickets por mes
GET	    /reports/avg-resolution/	   Obtiene el tiempo promedio de resolución

### Ejemplo de flujo para creación de ticket

POST /api/tickets/

        │
        ▼
Django REST Framework
        │
        ├── Validación
        ├── Autenticación
        ├── Autorización
        └── Persistencia
                │
                ▼
          PostgreSQL

---

## Autenticación y autorización

La API implementa mecanismos de autenticación y autorización para controlar el acceso a los diferentes recursos.

Los permisos pueden utilizarse para diferenciar funcionalidades dependiendo del tipo de usuario o rol dentro de la plataforma.

> Ajustar esta sección según el mecanismo utilizado realmente: JWT, Session Authentication, Token Authentication, OAuth, etc.

---

## Base de datos

La aplicación utiliza **PostgreSQL** como sistema gestor de base de datos.

La infraestructura de datos se gestiona mediante **Supabase**.

---

## Integración con Gemini

El backend utiliza la API de **Google Gemini** para proporcionar funcionalidades de asistencia inteligente.

La integración sigue un flujo similar a:

Frontend
   │
   │ Consulta del usuario
   ▼
Django API
   │
   │ Construcción del contexto
   ▼
Gemini API
   │
   │ Respuesta generada
   ▼
Django API
   │
   ▼
Frontend

Las credenciales de la API se mantienen mediante variables de entorno y no forman parte del código fuente.

---

## Docker

El backend está preparado para ejecutarse mediante Docker.

Ejemplo:

```bash
docker compose up --build
```

Para ejecutar los servicios en segundo plano:

```bash
docker compose up -d
```

Para detener los servicios:

```bash
docker compose down
```

---

## Configuración

Crear un archivo `.env` a partir del archivo de ejemplo:

```bash
cp .env.example .env
```

Ejemplo de configuración:

```env
DEBUG=False

SECRET_KEY=your-secret-key

DATABASE_URL=your-database-url

GEMINI_API_KEY=your-gemini-api-key

ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Instalación local

### Requisitos

* Python 3.x
* Docker
* Docker Compose
* PostgreSQL o conexión a Supabase
* Git

Clonar el repositorio:

```bash
git clone https://github.com/JuliusGarcia28/UAS_Help_Desk-BackEnd

cd backend
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activarlo:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar migraciones:

```bash
python manage.py migrate
```

Iniciar servidor:

```bash
python manage.py runserver
```

La API estará disponible normalmente en:

```text
http://localhost:8000/
```

---

## Integración con Frontend

El frontend Angular consume la API mediante solicitudes HTTP.

```text
┌───────────────────┐
│ Angular / Electron│
└─────────┬─────────┘
          │
          │ HTTP / JSON
          ▼
┌───────────────────┐
│   Django REST API │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ PostgreSQL/Supabase│
└───────────────────┘
```

La comunicación utiliza JSON como formato principal de intercambio de información.

---

## Despliegue

El backend puede ser desplegado mediante contenedores Docker.

La configuración de producción debe incluir:

* Variables de entorno seguras.
* `DEBUG=False`.
* Configuración adecuada de `ALLOWED_HOSTS`.
* Gestión segura de secretos.
* HTTPS.
* Configuración de CORS.
* Base de datos PostgreSQL.
* Logs y monitoreo.

---

## Seguridad

Entre las principales consideraciones de seguridad se encuentran:

* Gestión de secretos mediante variables de entorno.
* Validación de datos recibidos por la API.
* Autenticación de usuarios.
* Control de permisos.
* Configuración de CORS.
* Protección de credenciales.
* Uso de HTTPS en producción.
* Separación de configuraciones por ambiente.

---

## Autor

**Julian Javier Garcia Alvarez**

Desarrollador de software enfocado en desarrollo web, APIs, automatización e integración de soluciones.

---