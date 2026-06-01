# COTIZACIÓN DE SERVICIOS PROFESIONALES DE DESARROLLO DE SOFTWARE

**PROYECTO:** Plataforma de Seguridad Geolocalizada "SafeCampus UCB"  
**CLIENTE:** Universidad Católica Boliviana "San Pablo" - Regional Santa Cruz  
**ATENCIÓN:** Ing. Carlos Mendoza (Director del Depto. de Tecnologías y Seguridad)  
**FECHA:** 15 de abril de 2026  
**PROVEEDOR:** Equipo SCHEIBE (Contacto: Hernan Enrique Molina - enrique.molina@ucb.edu.bo)  
**ESTADO:** Aprobada y Firmada

---

## 1. DESCRIPCIÓN DEL PROYECTO
Desarrollo de un sistema de seguridad digital geolocalizado en tiempo real para proteger a la comunidad universitaria de la U.C.B. Regional Santa Cruz. La solución consta de un aplicativo web móvil para estudiantes (registro con correo institucional, geolocalización, mapa de acompañamiento anónimo y botón SOS) y una consola web de escritorio para el personal de monitoreo y seguridad (panel de control en tiempo real, mapa de incidentes y reporte estadístico de zonas críticas).

---

## 2. DESGLOSE DEL ESQUEMA TÉCNICO Y COSTOS

| Módulo / Componente | Descripción Técnica | Entregables | Costo (Bs.) |
| :--- | :--- | :--- | :---: |
| **Módulo 1: Arquitectura y Base de Datos** | Diseño del modelo relacional en MySQL 8. Estructuración del servidor Flask en Python 3.10. Configuración del hashing de contraseñas mediante bcrypt (12 rounds) para seguridad robusta de la información. | Script SQL de creación, configuración de conexión parametrizada y middleware de protección de rutas. | **Bs. 1,000.00** |
| **Módulo 2: Autenticación y Verificación** | Registro restringido al dominio `@ucb.edu.bo` (US 01). Login seguro (US 02) y verificación de cuenta por código único de 6 dígitos generado por el backend (US 04). Gestión de perfil de usuario y contactos de emergencia (US 05, US 16). | Vistas HTML de login/registro, algoritmo de generación de código OTP, y base de datos con flags de verificación. | **Bs. 1,000.00** |
| **Módulo 3: Mapa y Geolocalización** | Integración del API Leaflet y OpenStreetMap (US 06). Mecanismo de actualización periódica (polling de 10s) de latitud y longitud (US 07). API REST `/api/ubicacion` (US 08). Mapeo de usuarios cercanos en un radio de 500m de forma totalmente anónima (US 09). | Mapa interactivo del campus UCB, geoposicionamiento en el navegador cliente, e indexación espacial de coordenadas. | **Bs. 1,200.00** |
| **Módulo 4: Botón SOS y Monitoreo de Rescatista** | Interfaz del botón rojo de pánico (US 11) con confirmación previa. API `/api/alerta` (US 12). Panel con el estatus detallado de los rescatistas asignados (distancia, vehículo, miniruta Leaflet y barra de progreso de llegada) (US 14). | Frontend reactivo de pánico, sistema de cola de emergencias y visualización de llegada del personal de rescate. | **Bs. 1,200.00** |
| **Módulo 5: Consola de Monitoreo de Seguridad** | Panel de administración web para vigilantes (US 13). Vista en mapa de todas las alertas activas con pines parpadeantes. Notificaciones sonoras e intermitencia visual ante nuevas emergencias. Botón de atención y clasificación (atendida / falsa alarma). | Consola administrativa web optimizada para pantallas grandes, sonido y triggers visuales, y lógica de cierre de alertas. | **Bs. 800.00** |
| **Módulo 6: Dashboard Estadístico y Exportación** | Dashboard analítico para gerencia (Chart.js) que muestra total de alertas, tasa de falsas alarmas y tiempo de respuesta. Gráficos de distribución de alertas por zona del campus y por hora. Historial con filtros y exportación a CSV (US 15). | Interfaz gráfica de reportes con filtros interactivos de fechas, gráficos dinámicos y generador de archivos CSV en caliente. | **Bs. 800.00** |

### **TOTAL DEL PROYECTO: Bs. 6,000.00 (Seis Mil 00/100 Bolivianos)**

---

## 3. ENTREGABLES INCLUIDOS
*   Código fuente completo en un repositorio privado de GitHub, con acceso cedido al cliente.
*   Script SQL para la recreación e inicialización de la base de datos MySQL.
*   Manual de instalación rápida e instrucciones de despliegue local y en la nube.
*   Sesión de capacitación de 2 horas para el personal de monitoreo de seguridad del campus.
*   Garantía de soporte técnico post-entrega por 30 días para corrección de bugs.

---

## 4. TÉRMINOS Y CONDICIONES
*   **Vigencia de la Cotización:** 30 días calendario a partir de su emisión.
*   **Forma de Pago:** 50% de anticipo al aceptar la cotización y firmar contrato (Bs. 3,000.00); 50% al finalizar la entrega, despliegue y capacitación (Bs. 3,000.00).
*   **Medio de Pago:** Transferencia electrónica directa a cuenta BNB N° 123-456789-0-12 (Titular: Hernan Enrique Molina).
*   **Tiempo de Ejecución:** 6 semanas desde la recepción del anticipo.

<br><br>

| Aprobado por el Cliente | Presentado por el Proveedor |
| :---: | :---: |
| <br><br>____________________________________ <br> **Ing. Carlos Mendoza** <br> Director del Depto. de Tecnologías y Seguridad <br> U.C.B. Regional Santa Cruz | <br><br>____________________________________ <br> **Hernan Enrique Molina** <br> Desarrollador Frontend / Representante <br> Equipo SCHEIBE |
