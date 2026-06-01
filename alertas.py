"""
alertas.py - Sistema de alertas SOS de SafeCampus UCB
CORE del proyecto - Cubre:
  - US 11 (boton de panico UI)
  - US 12 (envio de alerta al servidor) <-- KEVIN BACKEND
  - US 13 (panel de monitoreo)          <-- KEVIN BACKEND (Sprint 3)
  - US 14 (confirmacion de alerta enviada)
  - US 15 (historial de alertas)
"""

from conexion import ejecutar_query


def emitir_alerta(usuario_id, latitud, longitud):
    """
    US 12 - Envio de alerta al servidor.

    El estudiante activa el boton de panico y se registra la alerta
    con su ubicacion exacta.

    Criterios:
    - Recibe ID estudiante, latitud, longitud
    - Procesa en menos de 2 segundos
    """
    if latitud is None or longitud is None:
        return {'ok': False, 'mensaje': 'Coordenadas requeridas para la alerta'}

    try:
        lat = float(latitud)
        lng = float(longitud)
    except (TypeError, ValueError):
        return {'ok': False, 'mensaje': 'Coordenadas invalidas'}

    # Verificar que no haya una alerta activa del mismo usuario (evitar duplicados)
    activa = ejecutar_query(
        """SELECT id FROM alertas
           WHERE usuario_id = %s AND estado = 'activa'""",
        (usuario_id,),
        fetch=True
    )
    if activa:
        return {
            'ok': False,
            'mensaje': 'Ya tienes una alerta activa pendiente de atencion',
            'alerta_id': activa[0]['id']
        }

    # Crear la alerta
    nuevo_id = ejecutar_query(
        """INSERT INTO alertas (usuario_id, latitud, longitud, estado)
           VALUES (%s, %s, %s, 'activa')""",
        (usuario_id, lat, lng),
        fetch=False
    )

    return {
        'ok': True,
        'mensaje': 'Alerta enviada. El centro de monitoreo fue notificado.',
        'alerta_id': nuevo_id
    }


def listar_alertas_activas():
    """
    US 13 - Panel de administracion (Monitoreo).  <-- TU US DEL SPRINT 3

    Devuelve la lista de alertas activas con datos del estudiante.

    Criterios:
    - Tabla con: nombre, ubicacion, hora de la alerta
    - Boton para marcar como atendida (US 13)
    """
    query = """
        SELECT
            a.id            AS alerta_id,
            a.latitud,
            a.longitud,
            a.fecha_emision,
            a.estado,
            u.id            AS usuario_id,
            u.nombre        AS nombre_estudiante,
            u.correo        AS correo_estudiante,
            u.telefono      AS telefono_estudiante,
            TIMESTAMPDIFF(MINUTE, a.fecha_emision, NOW()) AS minutos_transcurridos
        FROM alertas a
        INNER JOIN usuarios u ON a.usuario_id = u.id
        WHERE a.estado = 'activa'
        ORDER BY a.fecha_emision DESC
    """
    return ejecutar_query(query, fetch=True) or []


def marcar_alerta_atendida(alerta_id, monitor_id, falsa_alarma=False):
    """
    US 13 - Boton "marcar como atendida".

    El monitor cierra la alerta. Se registra quien la cerro y cuando.
    """
    estado_nuevo = 'falsa_alarma' if falsa_alarma else 'atendida'

    filas = ejecutar_query(
        """UPDATE alertas
           SET estado = %s, fecha_cierre = NOW(), monitor_id = %s
           WHERE id = %s AND estado = 'activa'""",
        (estado_nuevo, monitor_id, alerta_id),
        fetch=False
    )

    if filas and filas > 0:
        return {
            'ok': True,
            'mensaje': f'Alerta marcada como {estado_nuevo}'
        }

    return {'ok': False, 'mensaje': 'Alerta no encontrada o ya fue atendida'}


def listar_historial_alertas(filtro_estado=None, usuario_id=None):
    """
    US 15 - Historial de alertas (Audit).

    Permite filtrar por estado (atendida/falsa_alarma) o por usuario.
    """
    query = """
        SELECT
            a.id            AS alerta_id,
            a.latitud,
            a.longitud,
            a.fecha_emision,
            a.fecha_cierre,
            a.estado,
            u.nombre        AS nombre_estudiante,
            u.correo        AS correo_estudiante,
            m.nombre        AS nombre_monitor
        FROM alertas a
        INNER JOIN usuarios u ON a.usuario_id = u.id
        LEFT JOIN usuarios m ON a.monitor_id = m.id
        WHERE 1=1
    """
    params = []

    if filtro_estado:
        query += " AND a.estado = %s"
        params.append(filtro_estado)

    if usuario_id:
        query += " AND a.usuario_id = %s"
        params.append(usuario_id)

    query += " ORDER BY a.fecha_emision DESC LIMIT 100"

    return ejecutar_query(query, tuple(params), fetch=True) or []


def contar_alertas_por_estado():
    """Cuenta alertas agrupadas por estado (para dashboard del monitor)."""
    return ejecutar_query(
        "SELECT estado, COUNT(*) AS total FROM alertas GROUP BY estado",
        fetch=True
    ) or []


if __name__ == "__main__":
    # Prueba: emitir alerta
    print("=== Test alertas ===")
    resultado = emitir_alerta(1, -17.7833, -63.1821)
    print(f"Emitir: {resultado}")

    activas = listar_alertas_activas()
    print(f"Activas: {len(activas)}")
    for a in activas:
        print(f"  - {a['nombre_estudiante']} @ ({a['latitud']}, {a['longitud']})")
