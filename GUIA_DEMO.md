# GUION DE DEMO - SafeCampus UCB
## Presentacion al docente - VERSION FINAL ACTUALIZADA

---

## ANTES DE EMPEZAR (5 minutos antes)

1. Abrir MySQL Workbench y verificar que el servicio MySQL este corriendo
2. Abrir CMD en la carpeta del proyecto y ejecutar: `python app.py`
3. Abrir **DOS ventanas del navegador**:
   - **Ventana 1 (Chrome):** rol de ESTUDIANTE
   - **Ventana 2 (Edge u otra):** rol de MONITOR
4. Tener listo el flujo en la cabeza

---

## GUION PASO A PASO (15-20 minutos)

### Acto 1 - Presentacion (2 min) — Maximiliano (PO)

> "Buenos dias profesor. Somos el equipo SCHEIBE y presentamos **SafeCampus UCB**,
> un sistema de seguridad geolocalizada para los estudiantes de nuestra universidad.
>
> **El problema:** muchos estudiantes se sienten inseguros al salir tarde del campus.
> Nuestro sistema permite (1) ver companeros cercanos en un mapa para caminar
> acompanados, (2) activar un boton de panico que notifica al centro de monitoreo
> con ubicacion exacta, y (3) que el personal de seguridad responda en tiempo real
> desde su panel administrativo."

### Acto 2 - Arquitectura (2 min) — Kevin (Backend)

> "Stack tecnologico: Python con Flask para el backend, MySQL para datos,
> bcrypt con 12 rounds para hashing de passwords, OpenStreetMap con Leaflet
> para mapas, y Chart.js para los graficos del dashboard.
>
> Tenemos 4 tablas: usuarios, ubicaciones, alertas y contactos_emergencia.
> La comunicacion entre frontend y backend es via REST API con JSON.
> El polling se actualiza cada 5-10 segundos para tiempo real."

(Mostrar brevemente la BD en MySQL Workbench)

### Acto 3 - Registro y Verificacion (2 min) — Enrique (Frontend)

1. Ventana 1: ir a `/registro`
2. Llenar: `demo.estudiante@ucb.edu.bo` / `demo1234` / `Demo Estudiante`
3. Click Registrar

> "Validamos que el correo sea exclusivamente del dominio @ucb.edu.bo.
> Esto cumple la US 01: solo miembros de la UCB pueden registrarse.
>
> Generamos un codigo de verificacion de 6 digitos. En produccion se enviaria
> por correo institucional. Para la demo lo mostramos en pantalla."

4. Copiar codigo, pegar y verificar

> "La US 04 protege contra registros fraudulentos: la cuenta no se activa hasta
> demostrar acceso al correo institucional."

### Acto 4 - Login y Mapa con GPS (3 min) — Fernando (UX)

1. Login con `kevin.panoso@ucb.edu.bo` / `ucb1234`
2. Aceptar permisos de geolocalizacion

> "US 02: login exitoso. Las passwords estan hasheadas con bcrypt de 12 rounds,
> NO con MD5. Esto es critico en un sistema de seguridad.
>
> US 06: el mapa solicita permisos GPS y centra en mi ubicacion actual.
> US 07: cada 10 segundos hace polling automatico de mi posicion.
> US 08: cada coordenada se envia al backend via POST /api/ubicacion.
> US 09: vemos puntos verdes que son otros estudiantes cercanos en un radio
> de 500 metros, **anonimos** - no muestro nombre ni ID, solo posicion."

### Acto 5 - BOTON DE PANICO + RESCATISTAS (4 min) — CLIMAX — Fernando

1. Mostrar el boton rojo SOS
2. Click en SOS, confirmar

> "Aqui esta el corazon del sistema. US 11: boton rojo, grande, pide
> confirmacion para evitar falsas alarmas.
>
> US 12: dispara POST /api/alerta con mi ID, latitud, longitud y timestamp.
> El backend procesa en menos de 2 segundos."

3. Aparece automaticamente el card de RESCATISTAS EN CAMINO

> "**Aqui viene lo importante** (segun el prototipo que disene yo): no solo
> confirmamos al estudiante que la alerta fue enviada (US 14), sino que le
> mostramos en tiempo real **quien viene a ayudarlo, donde esta y cuanto
> tarda en llegar**.
>
> - Tipo de vehiculo: Ambulancia
> - Distancia: 2.3 km que se reduce
> - Mini mapa con la ruta del rescatista hacia el estudiante
> - Barra de progreso con tiempo restante
> - Push notification del navegador para que llegue incluso con la app en background
>
> Esto reduce drasticamente la ansiedad del estudiante en situacion de panico."

### Acto 6 - Panel de Monitoreo (3 min) — Kevin (Backend) — TU US

1. Ventana 2: login como `monitor.seguridad@ucb.edu.bo` / `ucb1234`

> "Cambiamos al rol de Monitor. **US 13: Panel de administracion**, la US que
> implemente en este Sprint 3.
>
> El monitor ve:
> - Lista de alertas activas con datos del estudiante
> - Telefono de contacto para llamar
> - Ubicacion exacta en coordenadas
> - Tiempo transcurrido desde la emision (con animacion de urgencia)
> - Mapa con pines rojos parpadeantes
>
> Se actualiza en tiempo real cada 5 segundos. Cuando entra una alerta nueva,
> el sistema avisa con sonido y flash visual."

2. Click en "Atender" en la alerta del paso 5

> "El monitor cierra la alerta. El sistema registra quien la cerro y a que hora.
> Esto es trazabilidad completa para auditoria."

### Acto 7 - DASHBOARD DE ALERTAS (3 min) — NUEVO — Mauro (QA)

1. Click en "Reportes" en el menu

> "Este es el **Dashboard de Alertas**, una pantalla que disenamos junto al
> equipo para que la administracion universitaria pueda tomar decisiones
> basadas en datos.
>
> Arriba tenemos:
> - **Filtros** por rango de fechas, estado y busqueda de estudiante
>
> En las tarjetas de stats:
> - Total de alertas historicas
> - Tasa de falsas alarmas (importante para evaluar el sistema)
> - Tiempo promedio de respuesta (KPI clave de seguridad)
> - Total de alertas atendidas con porcentaje
>
> Los graficos:
> - **Alertas por zona del campus**: Edificio A, B, Area Verde, Otro.
>   Esto permite ubicar mejor las rondas de seguridad.
> - **Alertas por hora del dia**: vemos los picos de incidencias para
>   reforzar personal en esas franjas.
>
> Abajo tabla con las ultimas alertas y boton de **exportar CSV** para
> reportes mensuales."

2. Probar un filtro: cambiar estado a "Falsa alarma" y aplicar

> "Los filtros funcionan dinamicamente. Esto es util para analisis especificos."

### Acto 8 - Historial y CSV (2 min) — Mauro

1. Click en "Historial"

> "US 15: historial completo con filtros por estado. Trazabilidad total."

2. Click en "Exportar CSV"

> "Para auditorias externas o reportes a la administracion universitaria."

### Acto 9 - Cierre (1 min) — Ernesto (SM)

> "Resumiendo, en este Sprint 3 entregamos:
>
> - **14 historias de usuario funcionales** del backlog de SafeCampus
> - **Stack moderno** y seguro (Python, Flask, bcrypt)
> - **Comunicacion en tiempo real** cliente-servidor
> - **Prototipos visuales** del equipo UX integrados al codigo
> - **Dashboard analitico** para toma de decisiones
>
> Para el Sprint 4 queda planificado:
> - US 03 (recuperacion de password)
> - Integracion real con SMS via Twilio
> - Notificaciones push nativas en mobile
>
> Estamos abiertos a preguntas."

---

## ASIGNACION DE ROLES

| Persona | Rol durante la demo |
|---|---|
| **Maximiliano (PO)** | Acto 1 (problema y mision) |
| **Kevin (Backend)** | Acto 2 (arquitectura), Acto 6 (panel monitoreo) |
| **Enrique (Frontend)** | Acto 3 (registro/login) |
| **Fernando (UX)** | Actos 4, 5 (mapa, boton de panico, rescatistas) |
| **Mauro (QA)** | Actos 7, 8 (dashboard, historial, CSV) |
| **Ernesto (SM)** | Acto 9 (cierre y preguntas) |

---

## PREGUNTAS QUE EL DOCENTE PROBABLEMENTE HARA

### "Por que bcrypt y no MD5?"
> "MD5 esta roto criptograficamente desde 2004. Vulnerable a rainbow tables
> y demasiado rapido para resistir fuerza bruta con GPU. En un sistema de
> SEGURIDAD seria contradictorio usarlo. Bcrypt con salt incluido y 12 rounds
> es el estandar actual."

### "Como aseguran la privacidad?"
> "En la US 09 (usuarios cercanos), el endpoint /api/cercanos solo devuelve
> latitud, longitud y distancia. Nunca expone IDs ni nombres. Solo el monitor
> en US 13 accede a datos personales, y solo cuando hay alerta ACTIVA."

### "Y los rescatistas que vimos son reales?"
> "Para esta demo simulamos el sistema de rescate. En produccion se integraria
> con los servicios reales de seguridad UCB y posiblemente con emergencias
> medicas. La arquitectura ya soporta esa integracion: el endpoint
> /api/alerta puede notificar a cualquier sistema externo via webhook."

### "Como escalan esto a miles de usuarios?"
> "Para el MVP usamos polling cada 5-10 segundos con indices SQL optimizados.
> Para produccion con miles de usuarios usariamos WebSockets en lugar de
> polling, cache Redis para ubicaciones en tiempo real, y consideracion de
> microservicios si la carga lo amerita."

### "Que es 'el dashboard' y por que lo necesitan?"
> "Es la herramienta de toma de decisiones de la administracion. Permite ver
> tendencias de seguridad: que zonas tienen mas alertas, en que horarios se
> concentran, cual es la tasa de falsas alarmas (importante para evaluar la
> efectividad del sistema), tiempo promedio de respuesta (KPI de calidad).
> Sin datos, el sistema de seguridad es ciego."

### "Como detectan falsas alarmas?"
> "El monitor desde el panel puede marcar una alerta como 'Falsa alarma'
> despues de contactar al estudiante. El sistema cuenta estas marcas y las
> reporta en el dashboard. Si la tasa sube mucho, sabemos que algo esta
> mal con el flujo (boton muy accesible, falta de educacion al usuario, etc.)."

---

## PLAN B SI ALGO FALLA EN VIVO

| Falla | Solucion |
|---|---|
| MySQL no conecta | Tener capturas/video de respaldo |
| Internet falla (mapas) | Los mapas requieren conexion. Tener video grabado de la demo |
| Browser no carga | Reiniciar Flask, abrir en modo incognito |
| GPS no da permisos | El sistema usa coordenadas del campus por defecto, sigue funcionando |
| Codigo de verificacion no aparece | Cerrar y volver a registrar con otro correo |

---

## CONSEJOS FINALES

1. **No leer la pantalla, hablarle al docente.** El que presenta debe mirar al docente, no a la pantalla.
2. **Si algo falla, no entrar en panico.** Decir "vamos a la siguiente parte y volvemos a esto despues".
3. **No improvisar codigo en vivo.** Si pide ver codigo, tener un editor abierto con el archivo listo.
4. **Cronometrar.** No pasar de 20 minutos. Mejor menos que mas.
5. **Ensayar al menos UNA VEZ completo antes de manana** con todos en llamada.
