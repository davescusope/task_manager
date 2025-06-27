# Gestor de Tareas (API Flask)

## Objetivo del proyecto

Este proyecto implementa una API REST para la gestión de tareas, permitiendo crear, consultar, actualizar y eliminar tareas. Está desarrollado en Python usando Flask y almacena los datos en un archivo JSON. Incluye funcionalidades de IA para enriquecer las tareas y se puede usar tanto desde la línea de comandos como desde una interfaz web.

## Instrucciones de instalación

1. **Clona el repositorio y accede a la carpeta del proyecto:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd task_manager
   ```

2. **Crea un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Iniciar el servidor

**IMPORTANTE**: Antes de ejecutar cualquier comando de la API, asegúrate de que el servidor esté en funcionamiento.

1. **Inicia el servidor con el siguiente comando:**
   ```bash
   python -m task_manager.app
   ```

2. **El servidor estará disponible en:** http://127.0.0.1:5000/

## Formas de uso

### 1. Interfaz Web (Recomendado)

La forma más sencilla de usar la aplicación es a través de la interfaz web:

1. Inicia el servidor como se indicó anteriormente
2. Abre tu navegador y ve a http://localhost:5000
3. Verás una interfaz intuitiva que te permite:
   - Ver todas las tareas existentes
   - Categorizar tareas usando IA
   - Estimar el esfuerzo de las tareas
   - Realizar auditorías de riesgos

### 2. Línea de comandos (PowerShell)

También puedes interactuar con la API usando PowerShell. Aquí tienes ejemplos de cada operación:

#### Obtener todas las tareas (GET)
```powershell
Invoke-RestMethod -Method GET -Uri "http://127.0.0.1:5000/tasks"
```

#### Crear una nueva tarea (POST)
```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    title = "Implementar autenticacion"
    description = "Desarrollar el sistema de login y registro de usuarios"
    status = "pendiente"
    effort_hours = 8
    priority = "alta"
    assigned_to = "desarrollador1"
} | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:5000/tasks" -Headers $headers -Body $body
```

#### Modificar una tarea existente (PUT)
```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    title = "Tarea Actualizada"
    description = "Nueva descripción"
    status = "en progreso"
    effort_hours = 4
    priority = "baja"
    assigned_to = "usuario"
} | ConvertTo-Json

Invoke-RestMethod -Method PUT -Uri "http://127.0.0.1:5000/tasks/1" -Headers $headers -Body $body
```

#### Eliminar una tarea (DELETE)
```powershell
Invoke-RestMethod -Method DELETE -Uri "http://127.0.0.1:5000/tasks/5"
```

#### Usar las funcionalidades de IA

##### Categorizar una tarea
```powershell
$body = @{
    task_id = 1
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:5000/ai/tasks/categorize" -Body $body -ContentType "application/json"
```

##### Estimar esfuerzo de una tarea
```powershell
$body = @{
    task_id = 1
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:5000/ai/tasks/estimate" -Body $body -ContentType "application/json"
```

##### Auditar una tarea
```powershell
$body = @{
    task_id = 1
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:5000/ai/tasks/audit" -Body $body -ContentType "application/json"
```

## Endpoints de Historias de Usuario

### Listar todas las historias de usuario (GET)

```powershell
Invoke-RestMethod -Method GET -Uri "http://localhost:5000/user-stories"
```

### Crear una historia de usuario a partir de un prompt (POST)

```powershell
Invoke-RestMethod -Method POST -Uri "http://localhost:5000/user-stories" -Body (@{prompt = 'Quiero una historia de usuario para un sistema de reservas de hoteles'} | ConvertTo-Json) -ContentType "application/json"
```

### Generar tareas para una historia de usuario (POST)

```powershell
Invoke-RestMethod -Method POST -Uri "http://localhost:5000/user-stories/ID/generate-tasks"
```
Reemplaza `ID` por el id de la historia de usuario para la que quieres generar tareas.

### Listar tareas de una historia de usuario (GET)

```powershell
Invoke-RestMethod -Method GET -Uri "http://localhost:5000/user-stories/ID/tasks"
```
Reemplaza `ID` por el id de la historia de usuario.

## Estructura de una tarea

Cada tarea incluye los siguientes campos:

- **id**: Identificador único de la tarea (número)
- **title**: Título de la tarea (string)
- **description**: Descripción detallada (string)
- **status**: Estado de la tarea ("pendiente", "en progreso", "completada")
- **effort_hours**: Horas estimadas de esfuerzo (número)
- **priority**: Prioridad de la tarea ("alta", "media", "baja")
- **assigned_to**: Usuario asignado a la tarea (string)
- **category**: Categoría de la tarea (string, opcional)
- **risk_analysis**: Análisis de riesgos (string, opcional)
- **risk_mitigation**: Plan de mitigación de riesgos (string, opcional)

## Códigos de respuesta

- **200 OK**: Operación exitosa
- **201 Created**: Tarea creada exitosamente
- **400 Bad Request**: Error en los datos enviados
- **404 Not Found**: Tarea no encontrada
- **500 Internal Server Error**: Error del servidor

# Gestor de Tareas con Asistente IA

Este proyecto es una aplicación en Python que permite gestionar tareas de manera interactiva utilizando un asistente inteligente basado en IA.

## ¿Cómo funciona?

- Al iniciar la aplicación, el usuario debe elegir una tarea existente del listado almacenado en `tasks.json` o puede inventar una nueva tarea en el momento.
- Si la tarea seleccionada no existe, el asistente guía al usuario para crear una nueva, solicitando los datos necesarios (título, descripción, prioridad, esfuerzo estimado, estado y asignado a).
- Actualmente, las nuevas tareas creadas durante la interacción **no se almacenan** en el archivo `tasks.json`. Si se requiere esta funcionalidad, se implementará en futuros entregables para acoplarse a los requisitos del entregable 1 y el entregable 2.
- Las tareas existentes se consultan desde el archivo `tasks.json`.

## Requisitos

- Python 3.8 o superior
- Paquetes: `openai`, `tiktoken`

## Uso

1. Ejecuta la aplicación.
2. Elige una tarea existente por su ID o crea una nueva siguiendo las instrucciones del asistente.
3. Las tareas existentes se leen desde `tasks.json`. Las nuevas tareas no se guardan automáticamente.

## Seguridad de la conexión a MySQL (Azure)

> **ATENCIÓN:**
> Actualmente la conexión a la base de datos MySQL de Azure está configurada para usar **SSL** con el certificado raíz de DigiCert, tal y como requiere Azure.
>
> El archivo de certificado `DigiCertGlobalRootG2.crt.pem` debe estar en la carpeta `task_manager`.
>
> El código de conexión en `app.py` está configurado así:
> ```python
> cert_path = os.path.join(os.path.dirname(__file__), 'DigiCertGlobalRootG2.crt.pem')
> connection_config = {
>     ...
>     'ssl': {'ca': cert_path}
> }
> ```
>
> Si tienes problemas de conexión SSL, asegúrate de que el archivo está presente y que la ruta es correcta. Consulta la documentación oficial de Azure Database for MySQL para más detalles sobre la configuración de SSL.

## Nota sobre despliegue en Docker

La variable de entorno `FLASK_APP` debe ser `task_manager.app` porque el archivo principal ahora está en el subdirectorio `task_manager/`. El Dockerfile ya está preparado para esto.

---