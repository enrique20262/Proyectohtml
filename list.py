"""
list.py - Listar usuarios de SafeCampus UCB
"""

from conexion import ejecutar_query


def listar_usuarios(solo_activos=False):
    """
    Devuelve la lista de todos los usuarios registrados.

    Args:
        solo_activos: si True, solo devuelve los que tienen estado='activo'

    Returns:
        lista de dicts con: id, correo, nombre, telefono, rol, is_verified, estado
    """
    query = """
        SELECT id, correo, nombre, telefono, rol, is_verified, estado, created_at
        FROM usuarios
    """
    if solo_activos:
        query += " WHERE estado = 'activo'"
    query += " ORDER BY id ASC"

    return ejecutar_query(query, fetch=True) or []


def obtener_usuario_por_id(usuario_id):
    """Obtiene un usuario especifico por ID (sin password)."""
    resultado = ejecutar_query(
        """SELECT id, correo, nombre, telefono, rol, is_verified, estado, created_at
           FROM usuarios WHERE id = %s""",
        (usuario_id,),
        fetch=True
    )
    return resultado[0] if resultado else None


def obtener_usuario_por_correo(correo):
    """Obtiene un usuario especifico por correo."""
    resultado = ejecutar_query(
        """SELECT id, correo, nombre, telefono, rol, is_verified, estado
           FROM usuarios WHERE correo = %s""",
        (correo,),
        fetch=True
    )
    return resultado[0] if resultado else None


if __name__ == "__main__":
    usuarios = listar_usuarios()
    print(f"Total usuarios: {len(usuarios)}")
    for u in usuarios:
        print(f"  - {u['id']}: {u['correo']} ({u['rol']}) - {u['estado']}")
