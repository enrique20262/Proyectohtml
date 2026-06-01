# CONTRATO DE PRESTACIÓN DE SERVICIOS DE DESARROLLO DE SOFTWARE

Conste por el presente documento privado un **Contrato de Prestación de Servicios de Desarrollo de Software** (en adelante, el "Contrato"), celebrado al amparo de las leyes de la República de Bolivia, bajo los términos y condiciones siguientes:

---

## 1. PARTES CONTRATANTES

*   **EL DESARROLLOR (REPRESENTANTE DEL EQUIPO):**
    **Hernan Enrique Molina**, con C.I. [Número de C.I.] SC, de nacionalidad boliviana, estudiante de la carrera de Ingeniería de Sistemas de la Universidad Católica Boliviana "San Pablo" (U.C.B.) Regional Santa Cruz, actuando en representación del equipo de desarrollo **SCHEIBE** (integrado adicionalmente por Ernesto Castedo, Maximiliano Cancino, Fernando Quiroz, Kevin Yeison Panoso y Mauro Chinellato), en adelante denominado como el **"DESARROLLADOR"**.
    
*   **EL CLIENTE:**
    La **Universidad Católica Boliviana "San Pablo" - Regional Santa Cruz** (U.C.B.), con NIT 1020304050, representada legalmente en este acto por el **Ing. Carlos Mendoza**, en su calidad de Director del Departamento de Tecnologías y Seguridad de la U.C.B. Regional Santa Cruz, con oficina administrativa en la Av. Busch, entre 2do y 3er Anillo, Santa Cruz de la Sierra, Bolivia, en adelante denominada como el **"CLIENTE"**.

Ambas partes, reconociéndose la capacidad legal necesaria para contratar y obligarse, convienen libre y voluntariamente en celebrar el presente Contrato.

---

## 2. OBJETO DEL CONTRATO
El objeto del presente Contrato es la prestación de servicios profesionales para el diseño, desarrollo, pruebas e implementación de la plataforma web denominada **"SafeCampus UCB"**. 

El sistema consiste en un MVP (Producto Mínimo Viable) de seguridad geolocalizada diseñado para la comunidad universitaria, el cual permite la visualización de la posición del usuario en un mapa interactivo (OpenStreetMap + Leaflet), el registro y mapeo anónimo de usuarios cercanos en un radio de 500 metros para fomentar el acompañamiento seguro, la activación de un Botón de Pánico (SOS) con transmisión de coordenadas en tiempo real al servidor, y un Panel de Monitoreo con Dashboard Analítico para el personal de seguridad de la U.C.B.

---

## 3. ESPECIFICACIONES TÉCNICAS Y ENTREGABLES
El **DESARROLLADOR** se compromete a entregar la plataforma estructurada de la siguiente manera:
1.  **Módulo de Autenticación y Perfil:** Registro de usuarios restringido a dominios institucionales (`@ucb.edu.bo`), Login seguro con cifrado Bcrypt (12 rounds) y verificación en dos pasos (código de 6 dígitos), edición de perfil y configuración de contactos de emergencia.
2.  **Módulo de Geolocalización en Tiempo Real:** Integración con Leaflet Maps y OpenStreetMap, captura de coordenadas GPS y polling periódico de ubicación (cada 10 segundos).
3.  **Módulo SOS (Botón de Pánico):** Emisión instantánea de alertas de emergencia al backend, guardando coordenadas precisas y notificando al usuario del estatus del rescatista.
4.  **Módulo Administrativo (Monitor):** Panel de control en tiempo real para visualizar y gestionar alertas activas, cerrar incidencias y clasificar falsas alarmas con sonido e interfaces dinámicas.
5.  **Dashboard de Reportes y Auditoría:** Gráficos analíticos de incidencias por zona y hora, estadísticas de rendimiento (KPIs como tiempo de respuesta, tasa de falsas alarmas) y exportación de datos a formato CSV.

---

## 4. PLAZO DE ENTREGA
Las partes acuerdan que el desarrollo del proyecto se ejecutará en un plazo de **6 semanas**, estructurado bajo metodología ágil Scrum en 3 Sprints quincenales, iniciándose el **20 de abril de 2026** y finalizando con la entrega formal y demostración en vivo el **1 de junio de 2026**.

---

## 5. PRECIO Y FORMA DE PAGO
Como contraprestación por los servicios de desarrollo descritos, el **CLIENTE** abonará al **DESARROLLADOR** la suma total y cerrada de **Bs. 6,000.00 (Seis Mil 00/100 Bolivianos)**, exenta de retenciones de ley bajo la modalidad de consultoría académica/profesional, pagadera bajo el siguiente cronograma:
*   **50% (Bs. 3,000.00):** A la firma del presente Contrato en calidad de anticipo para el inicio de las actividades (Pagado el 20 de abril de 2026).
*   **50% (Bs. 3,000.00):** Contra entrega total de la plataforma en funcionamiento, aprobación del cliente y capacitación básica al personal de seguridad (Pagado el 1 de junio de 2026).

Los pagos se realizarán mediante transferencia electrónica bancaria a la cuenta número **123-456789-0-12** del Banco Nacional de Bolivia (BNB), perteneciente a Hernan Enrique Molina.

---

## 6. PROPIEDAD INTELECTUAL Y CONFIDENCIALIDAD
*   **Propiedad Intelectual:** El código fuente, la base de datos MySQL, el diseño UX/UI y la documentación generada en el marco de este proyecto serán de propiedad exclusiva del **CLIENTE** una vez cancelado el 100% del monto acordado en la Cláusula Quinta.
*   **Confidencialidad:** El **DESARROLLADOR** se compromete a no divulgar información confidencial del **CLIENTE** obtenida durante la ejecución de los servicios, incluyendo credenciales, datos reales de estudiantes u operaciones del centro de monitoreo.

---

## 7. GARANTÍA Y SOPORTE POST-ENTREGA
El **DESARROLLADOR** otorga una garantía de soporte técnico y corrección de errores (bugs) sin costo adicional por un período de **30 días calendario** a partir de la firma de conformidad de entrega. Esta garantía cubre fallas en el código entregado, pero no incluye solicitudes de nuevas funcionalidades.

---

## 8. CONFORMIDAD Y FIRMAS
En señal de conformidad y aceptación con todos y cada uno de los términos del presente Contrato, las partes firman el presente documento en dos ejemplares de un mismo tenor y valor, en la ciudad de Santa Cruz de la Sierra, al 1 de junio de 2026.

<br><br>

| Por el Desarrollador (Equipo SCHEIBE) | Por el Cliente (U.C.B.) |
| :---: | :---: |
| <br><br>____________________________________ <br> **Hernan Enrique Molina** <br> C.I. [Tu C.I.] SC <br> Desarrollador Frontend / Representante | <br><br>____________________________________ <br> **Ing. Carlos Mendoza** <br> Director del Depto. de Tecnologías y Seguridad <br> U.C.B. Regional Santa Cruz |
