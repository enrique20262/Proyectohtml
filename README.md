# SafeCampus UCB

Sistema de seguridad geolocalizada para la comunidad UCB.
Proyecto academico - Equipo **SCHEIBE** (Grupo 5) - Sprint 3.

---

## Equipo

| Miembro | Rol |
|---|---|
| Ernesto Castedo | Scrum Master |
| Maximiliano Cancino | Product Owner |
| Enrique Molina | Frontend |
| Fernando Quiroz | UX Designer |
| Kevin Yeison Panoso | **Backend** |
| Mauro Chinellato | QA / Logic |

---

## Stack tecnologico

- **Lenguaje:** Python 3.10+
- **Framework web:** Flask 3.0
- **Base de datos:** MySQL 8
- **Hashing de passwords:** bcrypt (12 rounds)
- **Mapas:** OpenStreetMap + Leaflet
- **Estilos:** CSS3 puro

---

## Historias de usuario implementadas

| US | Descripcion | Estado |
|----|-------------|--------|
| US 01 | Registro de Usuario con validacion dominio @ucb.edu.bo | ✅ |
| US 02 | Inicio de Sesion (Login) | ✅ |
| US 04 | Validacion de cuenta con codigo de 6 digitos | ✅ |
| US 05 | Edicion de perfil (nombre + telefono) | ✅ |
| US 06 | Visualizacion de posicion en mapa | ✅ |
| US 07 | Actualizacion automatica de ubicacion (polling 10s) | ✅ |
| US 08 | API de coordenadas | ✅ |
| US 09 | Visualizacion de usuarios cercanos (anonimos, radio 500m) | ✅ |
| US 10 | Logs de ubicacion para auditoria | ✅ |
| US 11 | Boton de panico (UI) | ✅ |
| US 12 | Envio de alerta SOS al backend | ✅ |
| US 13 | Panel de administracion (Monitoreo en tiempo real) | ✅ |
| US 14 | Confirmacion visual de alerta enviada | ✅ |
| US 15 | Historial de alertas con filtros | ✅ |
| US 16 | Configuracion de contactos de emergencia | ✅ |

**Pendientes para Sprint 4:**
- US 03 (Recuperacion de password via correo)
- Integracion SMS con Twilio
- Notificaciones push

---

## Estructura del proyecto

```
safecampus/
├── app.py                      # Servidor Flask (web)
├── main.py                     # Menu CLI (terminal)
├── conexion.py                 # Conexion MySQL
├── seguridad.py                # Hashing bcrypt + validaciones
├── login.py                    # Autenticacion (US 01, 02, 04)
├── insert.py                   # Insercion de usuarios
├── update.py                   # Actualizacion (US 05)
├── delete.py                   # Baja logica
├── list.py                     # Listado de usuarios
├── ubicaciones.py              # Ubicaciones (US 06, 07, 08, 09, 10)
├── alertas.py                  # SOS y monitoreo (US 11, 12, 13, 14, 15)
├── contactos.py                # Contactos emergencia (US 16)
├── reportes.py                 # Reportes y CSV
├── database.sql                # Script de creacion de BD
├── requirements.txt            # Dependencias Python
├── static/
│   └── style.css               # Estilos
└── templates/                  # Vistas HTML
    ├── layout.html
    ├── login.html
    ├── registro.html
    ├── verificar.html
    ├── mapa.html
    ├── perfil.html
    ├── panel_monitoreo.html
    ├── historial.html
    ├── usuarios.html
    └── reportes.html
```

---

## Instalacion rapida

```bash
# 1. Crear la base de datos
mysql -u root -p < database.sql

# 2. Configurar conexion (editar conexion.py si tienes password en MySQL)

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Arrancar el servidor web
python app.py

# 5. Abrir en navegador
# http://127.0.0.1:5000
```

Para instalacion detallada, ver **GUIA_INSTALACION.md**
Para el guion de la demo, ver **GUIA_DEMO.md**

---

## Usuarios de prueba

| Correo | Password | Rol |
|---|---|---|
| kevin.panoso@ucb.edu.bo | ucb1234 | Estudiante |
| maria.lopez@ucb.edu.bo | ucb1234 | Estudiante |
| juan.perez@ucb.edu.bo | ucb1234 | Estudiante |
| ana.gomez@ucb.edu.bo | ucb1234 | Estudiante |
| **monitor.seguridad@ucb.edu.bo** | **ucb1234** | **Monitor** |

---

## Endpoints API

| Metodo | Ruta | US | Descripcion |
|--------|------|----|----|
| POST | /api/ubicacion | US 08 | Registrar coordenadas |
| GET | /api/cercanos | US 09 | Usuarios cercanos anonimos |
| POST | /api/alerta | US 12 | Activar boton de panico |
| GET | /api/alertas-activas | US 13 | Listar alertas para monitor |

---

## Seguridad

- **Passwords:** hasheadas con bcrypt 12 rounds (NO MD5)
- **Validacion de dominio:** solo @ucb.edu.bo permitido
- **Verificacion 2 pasos:** login bloqueado hasta validar codigo
- **Anonimato:** /api/cercanos no expone IDs ni nombres
- **SQL Injection:** todas las queries usan parametros preparados
- **Sesiones:** Flask sessions con secret_key seguro
- **Autorizacion por rol:** solo monitores ven el panel SOS

---

## Notas finales

Este proyecto es academico y simula un MVP. Para uso real:
- Sustituir polling por WebSockets
- Integrar SMTP real para verificaciones (no mostrar codigo en pantalla)
- Integrar Twilio para SMS de emergencia
- Cifrado en transito (HTTPS) obligatorio
- Variables de entorno via .env (no hardcoded)
