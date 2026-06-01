"""
reportes.py - Estadisticas y reportes de SafeCampus UCB
Equipo SCHEIBE - Sprint 3
"""

from conexion import ejecutar_query


def stats_dashboard():
    """
    Estadisticas principales del dashboard (imagen 2 del prototipo).
    Retorna: total_alertas, falsas_alarmas, tiempo_promedio, atendidas, variaciones.
    """
    # Total alertas
    total = ejecutar_query(
        "SELECT COUNT(*) AS total FROM alertas",
        fetch=True
    )
    total_alertas = total[0]['total'] if total else 0

    # Falsas alarmas
    falsas = ejecutar_query(
        "SELECT COUNT(*) AS total FROM alertas WHERE estado = 'falsa_alarma'",
        fetch=True
    )
    falsas_alarmas = falsas[0]['total'] if falsas else 0

    # Atendidas
    atendidas = ejecutar_query(
        "SELECT COUNT(*) AS total FROM alertas WHERE estado = 'atendida'",
        fetch=True
    )
    total_atendidas = atendidas[0]['total'] if atendidas else 0

    # Tiempo promedio de respuesta (en minutos)
    tiempo = ejecutar_query(
        """SELECT AVG(TIMESTAMPDIFF(MINUTE, fecha_emision, fecha_cierre)) AS promedio
           FROM alertas
           WHERE fecha_cierre IS NOT NULL""",
        fetch=True
    )
    tiempo_promedio = round(tiempo[0]['promedio'], 1) if tiempo and tiempo[0]['promedio'] else 0

    # Tasas
    tasa_falsas = round((falsas_alarmas / total_alertas * 100), 1) if total_alertas else 0
    tasa_atendidas = round((total_atendidas / total_alertas * 100), 1) if total_alertas else 0

    return {
        'total_alertas': total_alertas,
        'falsas_alarmas': falsas_alarmas,
        'tasa_falsas': tasa_falsas,
        'tiempo_promedio': tiempo_promedio,
        'atendidas': total_atendidas,
        'tasa_atendidas': tasa_atendidas,
    }


def alertas_por_zona():
    """
    Agrupa alertas por 'zona' del campus (imagen 1 del prototipo).
    Como aun no tenemos campo 'zona', se infiere de las coordenadas.

    Zonas del campus UCB Santa Cruz:
    - Edificio A: -17.7833, -63.1821 (radio ~50m)
    - Edificio B: -17.7835, -63.1819 (radio ~50m)
    - Area Verde: -17.7831, -63.1823 (radio ~50m)
    - Otro: cualquier otra ubicacion
    """
    alertas = ejecutar_query(
        "SELECT latitud, longitud FROM alertas",
        fetch=True
    ) or []

    zonas = {'Edificio A': 0, 'Edificio B': 0, 'Area Verde': 0, 'Otro': 0}

    # Centros aproximados (en realidad sirve cualquier criterio para la demo)
    centros = {
        'Edificio A': (-17.7833, -63.1821),
        'Edificio B': (-17.7835, -63.1819),
        'Area Verde': (-17.7831, -63.1823),
    }

    for a in alertas:
        lat = float(a['latitud'])
        lng = float(a['longitud'])
        zona_asignada = 'Otro'
        menor_dist = float('inf')

        for nombre, (clat, clng) in centros.items():
            # Distancia simple cuadrada (suficiente para clasificar)
            dist = (lat - clat) ** 2 + (lng - clng) ** 2
            if dist < menor_dist:
                menor_dist = dist
                # Si esta muy lejos (>0.001 = ~100m), va a "Otro"
                zona_asignada = nombre if dist < 0.000003 else 'Otro'

        zonas[zona_asignada] += 1

    return zonas


def alertas_por_hora():
    """
    Cuenta alertas agrupadas por hora del dia (imagen 1 del prototipo).
    Retorna lista de 24 valores (uno por cada hora 0-23).
    """
    resultados = ejecutar_query(
        """SELECT HOUR(fecha_emision) AS hora, COUNT(*) AS total
           FROM alertas
           GROUP BY HOUR(fecha_emision)
           ORDER BY hora""",
        fetch=True
    ) or []

    # Inicializar array de 24 horas en 0
    horas = [0] * 24
    for r in resultados:
        # Defensa: a veces MySQL devuelve la columna como tupla
        hora_key = r.get('hora') if isinstance(r, dict) else None
        if hora_key is None and isinstance(r, dict):
            # Si el alias no funciono, buscar la primera clave numerica
            for k in r:
                if 'hour' in k.lower() or 'hora' in k.lower():
                    hora_key = r[k]
                    break
        if hora_key is not None and 0 <= hora_key < 24:
            horas[hora_key] = r.get('total', 0)

    return horas


def alertas_recientes(limite=10):
    """
    Ultimas N alertas para la tabla del dashboard (imagen 1).
    Incluye ID formateado, fecha, estudiante, zona, estado, tiempo respuesta.
    """
    resultados = ejecutar_query(
        """SELECT
              a.id,
              a.latitud,
              a.longitud,
              a.fecha_emision,
              a.fecha_cierre,
              a.estado,
              u.nombre AS nombre_estudiante,
              u.id AS usuario_id,
              TIMESTAMPDIFF(MINUTE, a.fecha_emision, a.fecha_cierre) AS tiempo_respuesta
           FROM alertas a
           INNER JOIN usuarios u ON a.usuario_id = u.id
           ORDER BY a.fecha_emision DESC
           LIMIT %s""",
        (limite,),
        fetch=True
    ) or []

    # Determinar zona de cada alerta
    centros = {
        'Edificio A': (-17.7833, -63.1821),
        'Edificio B': (-17.7835, -63.1819),
        'Area Verde': (-17.7831, -63.1823),
    }

    for r in resultados:
        lat = float(r['latitud'])
        lng = float(r['longitud'])
        zona_asignada = 'Otro'
        menor_dist = float('inf')

        for nombre, (clat, clng) in centros.items():
            dist = (lat - clat) ** 2 + (lng - clng) ** 2
            if dist < menor_dist:
                menor_dist = dist
                zona_asignada = nombre if dist < 0.000003 else 'Otro'

        r['zona'] = zona_asignada
        r['id_formateado'] = f"#ALT-{r['id']:04d}"
        r['est_formateado'] = f"Est. {r['usuario_id']:04d}"

    return resultados


def filtrar_alertas(fecha_desde=None, fecha_hasta=None, estado=None, busqueda=None):
    """
    Filtra alertas segun los criterios del dashboard (imagen 2).
    """
    query = """
        SELECT
            a.id,
            a.latitud, a.longitud,
            a.fecha_emision,
            a.fecha_cierre,
            a.estado,
            u.id AS usuario_id,
            u.nombre AS nombre_estudiante,
            u.correo,
            TIMESTAMPDIFF(MINUTE, a.fecha_emision, a.fecha_cierre) AS tiempo_respuesta
        FROM alertas a
        INNER JOIN usuarios u ON a.usuario_id = u.id
        WHERE 1=1
    """
    params = []

    if fecha_desde:
        query += " AND DATE(a.fecha_emision) >= %s"
        params.append(fecha_desde)

    if fecha_hasta:
        query += " AND DATE(a.fecha_emision) <= %s"
        params.append(fecha_hasta)

    if estado and estado != 'todas':
        query += " AND a.estado = %s"
        params.append(estado)

    if busqueda:
        query += " AND (u.nombre LIKE %s OR u.correo LIKE %s OR u.id LIKE %s)"
        busq = f"%{busqueda}%"
        params.extend([busq, busq, busq])

    query += " ORDER BY a.fecha_emision DESC LIMIT 100"

    return ejecutar_query(query, tuple(params), fetch=True) or []


# Funciones antiguas que sigue usando la app
def reporte_usuarios_por_estado():
    return ejecutar_query(
        "SELECT estado, COUNT(*) AS total FROM usuarios GROUP BY estado",
        fetch=True
    ) or []


def reporte_alertas_por_estado():
    return ejecutar_query(
        "SELECT estado, COUNT(*) AS total FROM alertas GROUP BY estado",
        fetch=True
    ) or []


def reporte_zonas_riesgo():
    return ejecutar_query(
        """SELECT
              ROUND(latitud, 3) AS lat_aprox,
              ROUND(longitud, 3) AS lng_aprox,
              COUNT(*) AS total_alertas
           FROM alertas
           WHERE estado != 'falsa_alarma'
           GROUP BY lat_aprox, lng_aprox
           ORDER BY total_alertas DESC LIMIT 10""",
        fetch=True
    ) or []


def exportar_alertas_csv():
    alertas = ejecutar_query(
        """SELECT a.id, u.nombre, u.correo, a.latitud, a.longitud,
                  a.estado, a.fecha_emision, a.fecha_cierre
           FROM alertas a
           INNER JOIN usuarios u ON a.usuario_id = u.id
           ORDER BY a.fecha_emision DESC""",
        fetch=True
    ) or []

    lineas = ['ID,Estudiante,Correo,Latitud,Longitud,Estado,Fecha Emision,Fecha Cierre']
    for a in alertas:
        cierre = a['fecha_cierre'] if a['fecha_cierre'] else ''
        lineas.append(
            f"{a['id']},{a['nombre']},{a['correo']},"
            f"{a['latitud']},{a['longitud']},{a['estado']},"
            f"{a['fecha_emision']},{cierre}"
        )

    return '\n'.join(lineas)
