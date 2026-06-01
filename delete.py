"""
delete.py - Baja logica de usuarios SafeCampus UCB
NO se borra el registro fisicamente, solo se marca como inactivo.
Esto preserva el historial de alertas y ubicaciones para auditorias (US 10, US 15).
"""

from conexion import ejecutar_query


def desactivar_usuario(usuario_id):
    """
    Baja logica: marca al usuario como inactivo.
    No puede iniciar sesion pero conserva sus datos historicos.
    """
    # Verificar que existe
    existe = ejecutar_query(
        "SELECT id, estado FROM usuarios WHERE id = %s",
        (usuario_id,),
        fetch=True
    )

    if not existe:
        return {'ok': False, 'mensaje': 'Usuario no encontrado'}

    if existe[0]['estado'] == 'inactivo':
        return {'ok': False, 'mensaje': 'El usuario ya estaba inactivo'}

    # Baja logica
    ejecutar_query(
        "UPDATE usuarios SET estado = 'inactivo' WHERE id = %s",
        (usuario_id,),
        fetch=False
    )

    return {'ok': True, 'mensaje': 'Usuario desactivado correctamente'}


def reactivar_usuario(usuario_id):
    """Reactiva un usuario previamente desactivado."""
    filas = ejecutar_query(
        "UPDATE usuarios SET estado = 'activo' WHERE id = %s",
        (usuario_id,),
        fetch=False
    )

    if filas and filas > 0:
        return {'ok': True, 'mensaje': 'Usuario reactivado'}

    return {'ok': False, 'mensaje': 'No se pudo reactivar'}


if __name__ == "__main__":
    print(desactivar_usuario(2))
