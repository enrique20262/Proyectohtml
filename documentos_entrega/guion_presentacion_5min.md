# GUION DE PRESENTACIÓN INDIVIDUAL - 5 MINUTOS (ENRIQUE MOLINA)
**Rol: Desarrollador Frontend (Equipo SCHEIBE)**

Este guion está optimizado para durar exactamente **5 minutos**. Se enfoca en explicar el proyecto general, tus contribuciones específicas en el Frontend y el proceso ágil que siguió el equipo.

---

## CRONOGRAMA DE TIEMPO
*   **0:00 - 1:00 (1 Min):** Introducción y Contexto del Cliente.
*   **1:00 - 2:30 (1.5 Min):** Contribuciones Técnicas (Qué desarrollaste en Frontend).
*   **2:30 - 3:45 (1.25 Min):** El Proceso Metodológico (Trello, Git/GitHub y Scrum).
*   **3:45 - 4:30 (45 Seg):** Resultados y Relación con el Cliente (Contrato, Pago, Conformidad).
*   **4:30 - 5:00 (30 Seg):** Cierre y Preguntas.

---

## GUION PASO A PASO

### 1. Introducción y Contexto (0:00 - 1:00)
> *"Buenos días profesor y compañeros. Mi nombre es **Enrique Molina** y soy el desarrollador Frontend del equipo SCHEIBE. Hoy les presentaré el proyecto final que desarrollamos para nuestro cliente real: la **Universidad Católica Boliviana 'San Pablo' Regional Santa Cruz**, específicamente para su Departamento de Tecnologías y Seguridad.*
> 
> *El proyecto se denomina **SafeCampus UCB**, un sistema web móvil de seguridad geolocalizada en tiempo real. Nace de un problema real: la sensación de inseguridad y la falta de canales inmediatos cuando los estudiantes se desplazan por el campus o sus alrededores en horarios nocturnos. Nuestra solución permite a los estudiantes reportar emergencias geolocalizadas al instante y conectarse de manera coordinada con el centro de monitoreo del campus."*

---

### 2. Aportes Técnicos y de Frontend (1:00 - 2:30)
> *"(Mostrar las interfaces de la página web mientras hablas)*
> *En mi rol como Desarrollador Frontend, mi responsabilidad principal fue traducir los requerimientos y el diseño UX en componentes interactivos, responsivos y seguros utilizando **HTML5, CSS3 puro y JavaScript** integrado en el framework Flask.*
> 
> *Específicamente desarrollé:*
> 1. *Las **pantallas de registro y login** con validación estricta de dominios institucionales (`@ucb.edu.bo`) y el flujo visual de verificación en 2 pasos con código OTP.*
> 2. *La integración y renderizado del mapa dinámico utilizando **Leaflet y OpenStreetMap**, consumiendo la API REST del backend para graficar la ubicación GPS del usuario y mostrar puntos anónimos de estudiantes cercanos en un radio de 500 metros.*
> 3. *La interfaz del **Botón de Pánico (SOS)** y el flujo de confirmación visual en tiempo real que le indica al estudiante la ruta del rescatista, tipo de vehículo y barra de progreso de llegada.*
> 4. *La **consola administrativa de monitoreo** y el **Dashboard de analíticas** utilizando **Chart.js** para graficar incidencias por zona y hora, lo cual facilita la toma de decisiones al personal de seguridad de la UCB."*

---

### 3. El Proceso de Desarrollo y Herramientas (2:30 - 3:45)
> *"(Mostrar tu Trello y tu Git/GitHub en la pantalla)*
> *El éxito de este proyecto radica en el proceso metodológico que seguimos. Trabajamos bajo el marco de trabajo ágil **Scrum**, dividido en 3 sprints quincenales:*
> * En **Trello** estructuramos nuestro backlog con historias de usuario claras (desde la US 01 de registro hasta la US 16 de contactos). Monitoreamos diariamente las tareas en las columnas de 'To Do', 'In Progress', 'In Testing' y 'Done'.*
> * En **Git y GitHub** establecimos una estrategia de ramificación limpia. Trabajamos con ramas por funcionalidad (*feature branches*) y todo el código pasó por un proceso de revisión antes de mezclarse a la rama principal mediante *Pull Requests*. Esto garantizó la calidad y evitó conflictos de código en el equipo.*
> * Para garantizar que la base de datos MySQL y la lógica del servidor Flask interactuaran sin errores, implementamos pruebas de caja negra y automatizamos la inyección segura de parámetros para mitigar inyecciones SQL."*

---

### 4. Relación Comercial y Conformidad del Cliente (3:45 - 4:30)
> *"(Mostrar los documentos impresos: Contrato, Cotización, Comprobante y el Video)*
> *Para cumplir con las exigencias profesionales de la materia, formalizamos toda la relación comercial con nuestro cliente:*
> 1. *Presento aquí el **Contrato de Servicios** firmado, donde detallamos las responsabilidades, propiedad intelectual y cláusulas de confidencialidad.*
> 2. *La **Cotización Técnica** aprobada por un valor de **Bs. 6,000**, especificando el costo detallado por cada módulo de software.*
> 3. *El **Comprobante de Pago** electrónico que evidencia las transferencias bancarias de anticipo y liquidación en mi cuenta BNB.*
> 4. *Y finalmente, el **Video de Conformidad**, donde el Ing. Carlos Mendoza, representante del cliente, interactúa con la plataforma web desarrollada y expresa formalmente su satisfacción con el resultado final entregado."*

---

### 5. Cierre (4:30 - 5:00)
> *"Para cerrar, SafeCampus UCB demostró ser una solución real a un problema real, abordado con procesos de ingeniería de software profesionales. El cliente quedó muy satisfecho y el equipo adquirió experiencia práctica en el desarrollo ágil de software seguro.*
> 
> *Quedo abierto a cualquier pregunta que tenga sobre el desarrollo frontend, la geolocalización o el flujo del sistema. Muchas gracias."*

---

## CONSEJOS CLAVE PARA ENRIQUE
1.  **Ensaya con cronómetro:** Lee el guion en voz alta mientras navegas por la página y las diapositivas. Asegúrate de no correr ni pausar demasiado para clavar los 5 minutos.
2.  **Transiciones rápidas:** Practica abrir las pestañas de GitHub, Trello y los PDFs de contrato/cotización con anticipación para no perder segundos valiosos buscándolos.
3.  **Domina el tema de Frontend:** Si el docente te pregunta algo técnico, responde basándote en que usaste CSS3 puro para la responsividad, Leaflet.js para los mapas y peticiones Fetch asíncronas (`POST /api/ubicacion` con payload JSON) para comunicar la geolocalización sin recargar la página.
