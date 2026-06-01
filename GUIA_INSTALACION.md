# GUIA DE INSTALACION - SafeCampus UCB

> Para Windows + MySQL Workbench. Todo el equipo debe seguir estos pasos.

---

## Requisitos previos

- Windows 10 o superior
- MySQL Server corriendo (puede ser via Workbench, XAMPP o standalone)
- Python 3.10 o superior
- Navegador (Chrome, Edge o Firefox)

---

## PASO 1 — Instalar Python (si no lo tienes)

1. Ir a **https://www.python.org/downloads/**
2. Descargar **"Download Python 3.x.x"** (boton amarillo grande)
3. Ejecutar el instalador
4. **IMPORTANTE:** marcar la casilla `"Add Python to PATH"` antes de instalar
5. Click en **"Install Now"**
6. Verificar abriendo cmd y escribiendo:
   ```
   python --version
   ```
   Debe salir `Python 3.x.x`

---

## PASO 2 — Crear la base de datos

1. Abrir **MySQL Workbench**
2. Conectarse a `Local instance MySQL80` (o como se llame tu instancia)
3. Ir a **File → Open SQL Script**
4. Seleccionar el archivo `database.sql` del proyecto
5. Click en el rayo amarillo (Execute) o `Ctrl + Shift + Enter`
6. Deberia salir: `Base de datos SafeCampus creada exitosamente`

Para verificar:
1. En el panel izquierdo, refresh
2. Debe aparecer una base de datos `safecampus` con 4 tablas:
   - usuarios
   - ubicaciones
   - alertas
   - contactos_emergencia

---

## PASO 3 — Configurar la conexion

1. Abrir el archivo `conexion.py` con el Bloc de notas o VS Code
2. Editar la seccion `CONFIG_DB`:

```python
CONFIG_DB = {
    'host':     'localhost',
    'user':     'root',
    'password': '',              # <-- AQUI poner tu password de MySQL
    'database': 'safecampus',
    'port':     3306
}
```

3. Si tu MySQL no tiene password, dejar `password: ''`
4. Si tiene password, escribirla entre comillas
5. Guardar

---

## PASO 4 — Instalar dependencias de Python

1. Abrir cmd (Windows + R, escribir `cmd`)
2. Navegar a la carpeta del proyecto:
   ```
   cd C:\Users\TU_USUARIO\Desktop\safecampus
   ```
3. Instalar las librerias:
   ```
   pip install -r requirements.txt
   ```
4. Esperar a que termine (~1 minuto)

Si `pip` no funciona, intentar:
```
python -m pip install -r requirements.txt
```

---

## PASO 5 — Ejecutar el proyecto

### Opcion A — Version web (RECOMENDADA para la demo)

```
python app.py
```

Deberia salir:
```
============================================================
  SafeCampus UCB - Servidor Flask
  Equipo SCHEIBE - Sprint 3
============================================================
  Abre tu navegador en: http://127.0.0.1:5000
```

Abrir el navegador en **http://127.0.0.1:5000**

### Opcion B — Version CLI (terminal)

```
python main.py
```

Aparece un menu interactivo en la terminal.

---

## Usuarios de prueba para la demo

| Correo | Password | Rol |
|---|---|---|
| kevin.panoso@ucb.edu.bo | ucb1234 | Estudiante |
| maria.lopez@ucb.edu.bo | ucb1234 | Estudiante |
| juan.perez@ucb.edu.bo | ucb1234 | Estudiante |
| ana.gomez@ucb.edu.bo | ucb1234 | Estudiante |
| **monitor.seguridad@ucb.edu.bo** | **ucb1234** | **Monitor** |

---

## Solucion de problemas comunes

### "Access denied for user 'root'"
- Tu MySQL tiene password. Editar `conexion.py` y poner la correcta.

### "Can't connect to MySQL server"
- El servicio MySQL no esta corriendo.
- Abrir `services.msc`, buscar MySQL80, dar Start.

### "ModuleNotFoundError: No module named 'flask'"
- No se instalaron las dependencias.
- Correr: `pip install -r requirements.txt`

### "Address already in use" / "Port 5000 ocupado"
- Otro programa esta usando el puerto.
- Cerrar el otro programa, o cambiar el puerto en `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

### El mapa no muestra ubicacion real
- Permitir al navegador acceder al GPS.
- Si no, usa coordenadas del campus por defecto (esta OK para la demo).

### "Codigo de verificacion no llega por correo"
- Para la demo, el codigo aparece directamente en la pantalla despues del registro.
- En produccion se enviaria por correo institucional via SMTP.

---

## Detener el servidor

En la terminal donde corre el servidor: presionar `Ctrl + C`

---

## Reiniciar todo desde cero

Si quieres limpiar y empezar de nuevo:

1. En Workbench ejecutar:
   ```sql
   DROP DATABASE safecampus;
   ```
2. Volver a ejecutar `database.sql`
3. Reiniciar `app.py`
