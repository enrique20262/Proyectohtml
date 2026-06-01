"""
ubicaciones.py - Gestion de ubicaciones SafeCampus UCB
Cubre US 06 (visualizar posicion), US 07 (polling), US 08 (API coordenadas),
       US 09 (usuarios cercanos), US 10 (logs)
"""

from conexion import ejecutar_query
import math


def registrar_ubicacion(usuario_id, latitud, longitud):
    """
    US 08 - API de coordenadas.

    Registra la ubicacion actual del usuario en la base de datos.

    Criterios:
    - Recibe latitud, longitud
    - Valida que no sean nulos
    - Devuelve OK tras procesar
    """
    if latitud is None or longitud is None:
        return {'ok': False, 'mensaje': 'Latitud y longitud son requeridas'}

    try:
        lat = float(latitud)
        lng = float(longitud)
    except (TypeError, ValueError):
        return {'ok': False, 'mensaje': 'Coordenadas deben ser numericas'}

    # Validar rangos geograficos
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        return {'ok': False, 'mensaje': 'Coordenadas fuera de rango valido'}

    # US 10 - Persistir log de ubicacion
    nuevo_id = ejecutar_query(
        "INSERT INTO ubicaciones (usuario_id, latitud, longitud) VALUES (%s, %s, %s)",
        (usuario_id, lat, lng),
        fetch=False
    )

    return {
        'ok': True,
        'mensaje': 'Ubicacion registrada',
        'id': nuevo_id,
        'latitud': lat,
        'longitud': lng
    }


def obtener_ubicacion_actual(usuario_id):
    """
    US 06 - Devuelve la ultima ubicacion conocida del usuario.
    """
    resultado = ejecutar_query(
        """SELECT latitud, longitud, timestamp
           FROM ubicaciones
           WHERE usuario_id = %s
           ORDER BY timestamp DESC LIMIT 1""",
        (usuario_id,),
        fetch=True
    )
    return resultado[0] if resultado else None


def calcular_distancia(lat1, lng1, lat2, lng2):
    """
    Formula de Haversine para calcular distancia en metros entre dos puntos GPS.
    """
    R = 6371000  # radio de la Tierra en metros

    lat1_rad = math.radians(float(lat1))
    lat2_rad = math.radians(float(lat2))
    delta_lat = math.radians(float(lat2) - float(lat1))
    delta_lng = math.radians(float(lng2) - float(lng1))

    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def obtener_usuarios_cercanos(usuario_id, radio_metros=500):
    """
    US 09 - Visualizacion de usuarios cercanos.

    Criterios:
    - Marcadores de otros estudiantes
    - Radio de 500 metros
    - Datos ANONIMOS (solo posicion, sin nombre ni id)
    """
    # Obtener ultima ubicacion del usuario actual
    mi_ubicacion = obtener_ubicacion_actual(usuario_id)
    if not mi_ubicacion:
        return []

    # Obtener ultima ubicacion de TODOS los demas usuarios activos
    query = """
        SELECT u.usuario_id, u.latitud, u.longitud
        FROM ubicaciones u
        INNER JOIN (
            SELECT usuario_id, MAX(id) AS ultimo_id
            FROM ubicaciones
            GROUP BY usuario_id
        ) ultima ON u.id = ultima.ultimo_id
        WHERE u.usuario_id != %s
    """
    todos = ejecutar_query(query, (usuario_id,), fetch=True) or []

    # Filtrar por radio y devolver ANONIMOS
    cercanos = []
    for u in todos:
        distancia = calcular_distancia(
            mi_ubicacion['latitud'], mi_ubicacion['longitud'],
            u['latitud'], u['longitud']
        )
        if distancia <= radio_metros:
            cercanos.append({
                'latitud': float(u['latitud']),
                'longitud': float(u['longitud']),
                'distancia_metros': round(distancia)
            })

    cercanos.sort(key=lambda x: x['distancia_metros'])
    return cercanos


def limpiar_historico_antiguo(dias=30):
    """
    US 10 - Limpiar registros mayores a 30 dias.
    """
    filas = ejecutar_query(
        "DELETE FROM ubicaciones WHERE timestamp < DATE_SUB(NOW(), INTERVAL %s DAY)",
        (dias,),
        fetch=False
    )
    return filas or 0


if __name__ == "__main__":
    # Prueba
    resultado = registrar_ubicacion(1, -17.7833, -63.1821)
    print(f"Registrar: {resultado}")

    cercanos = obtener_usuarios_cercanos(1, radio_metros=500)
    print(f"Cercanos a Kevin: {len(cercanos)}")
    for c in cercanos:
        print(f"  - distancia: {c['distancia_metros']}m")
