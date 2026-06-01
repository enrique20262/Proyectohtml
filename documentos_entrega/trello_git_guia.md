# GUÍA DE CONFIGURACIÓN Y USO DE TRELLO Y GIT/GITHUB
**Puntaje de Herramientas de Proceso (Trello, Git/GitHub, Scrum)**

Para que el docente te asigne la máxima puntuación en el apartado de herramientas utilizadas durante el proceso de desarrollo, te recomiendo estructurar tu tablero de Trello y tu repositorio de GitHub de la siguiente manera. El docente buscará evidencia de trabajo en equipo, trazabilidad e ingeniería de software estructurada.

---

## I. ORGANIZACIÓN DEL TABLERO DE TRELLO

Un tablero de Trello profesional no solo tiene columnas de "Por hacer" y "Hecho", sino que refleja el flujo ágil completo y la división de tareas.

### 1. Estructura de Columnas Recomendada
1.  **Product Backlog (Pila del Producto):** Lista priorizada de todas las Historias de Usuario (US 01 a US 16).
2.  **Sprint Backlog (Sprint 3):** Tareas seleccionadas para este Sprint.
3.  **In Progress (En Progreso):** Tareas que se están desarrollando en este momento (deben tener asignados a los responsables).
4.  **In Testing / QA (En Pruebas):** Funcionalidades listas en código pero bajo revisión del QA (Mauro).
5.  **Done (Terminado):** Tareas validadas y finalizadas.

### 2. Formato de las Tarjetas (Cards)
Cada tarjeta debe ser clara y detallada.
*   **Título:** `US XX - [Título de la Historia de Usuario]` (Ej: *US 01 - Registro de Usuario con validación dominio @ucb.edu.bo*).
*   **Descripción:**
    ```text
    **Como** Estudiante de la UCB
    **Quiero** registrarme en el sistema
    **Para** poder acceder a las funciones de seguridad geolocalizada.
    
    **Criterios de Aceptación:**
    1. Validar que el correo tenga dominio @ucb.edu.bo.
    2. Hashear la contraseña con bcrypt antes de guardarla.
    3. Redirigir a la pantalla de verificación OTP.
    ```
*   **Miembros:** Asignar al responsable del desarrollo (ej: Enrique Molina para frontend, Kevin Panoso para backend).
*   **Etiquetas (Labels):** Utilizar colores para categorizar:
    *   `Frontend` (Verde)
    *   `Backend` (Azul)
    *   `Base de Datos` (Púrpura)
    *   `QA / Testing` (Naranja)
    *   `UX / Diseño` (Rosa)
*   **Adjuntos:** Sube capturas de pantalla de la interfaz final desarrollada o wireframes previos de Figma. Esto demuestra que la tarea fue finalizada con rigor estético.

---

## II. ESTRATEGIA DE TRABAJO EN GIT Y GITHUB

El docente entrará a tu GitHub a evaluar el historial de confirmaciones (*commits*) y la interacción de ramas. Si ve un único commit con todo el código subido al final, bajará puntos considerablemente.

### 1. Ramas del Proyecto (Git Flow Simplificado)
*   `main` (o `master`): Código estable de producción. Ningún desarrollador escribe código directo aquí.
*   `develop`: Rama de integración donde se consolidan las funcionalidades terminadas del Sprint.
*   `feature/USXX-descripcion`: Ramas individuales creadas para desarrollar una historia específica (ej: `feature/US01-registro` o `feature/US06-mapa-leaflet`).

### 2. Flujo de Trabajo con Pull Requests (PRs)
1.  El desarrollador termina la funcionalidad en su rama `feature/US01-registro`.
2.  Sube la rama a GitHub: `git push origin feature/US01-registro`.
3.  Crea un **Pull Request** de la rama `feature/US01-registro` hacia `develop`.
4.  **Code Review (Revisión de Código):** Otro miembro del equipo (por ejemplo, el Scrum Master Ernesto o el QA Mauro) revisa el código en GitHub, añade algún comentario si es necesario (ej: *"Excelente, validaste bien el regex del correo"*) y hace el **Approve** (Aprobación).
5.  Se realiza el **Merge** a `develop`.

*Esto deja un registro histórico en GitHub que el docente amará ver.*

### 3. Nomenclatura Profesional de Commits
Eviten commits genéricos como *"cambios"*, *"fix"*, *"listo"*. Utilicen el estándar Semantic Commits acoplado a las Historias de Usuario:
*   `feat(US01): crear pantalla de registro con estilo responsive CSS`
*   `fix(US02): corregir redirección de sesión inválida en login.py`
*   `docs(README): actualizar sección de instalación rápida y base de datos`
*   `test(US09): añadir pruebas unitarias para API de usuarios cercanos`

---

## III. CÓMO MOSTRAR TRELLO Y GITHUB EN LA EXPOSICIÓN (TIPS)

Cuando sea tu turno de presentar Trello y Git/GitHub (dentro de tus 5 minutos):
1.  **Tablero de Trello (15 segundos):** Muestra el tablero y resalta: *"Aquí está nuestro flujo de valor en Trello. Pueden ver cómo las historias de usuario pasaron por control de calidad antes de considerarse terminadas ('Done') con sus respectivos wireframes adjuntos"*.
2.  **GitHub Network Graph / PRs (15 segundos):** Entra a la pestaña de **Pull Requests** cerrados en tu repositorio y di: *"Usamos un flujo de integración ágil. Cada historia de usuario se desarrolló en una rama feature independiente y se integró mediante Pull Requests revisados por pares, lo que garantizó la calidad del código en producción"*.
