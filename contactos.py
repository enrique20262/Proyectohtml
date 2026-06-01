"""
contactos.py - Contactos de emergencia
Cubre US 16 - Configuracion de contactos de emergencia
"""

from conexion import ejecutar_query
from seguridad import validar_telefono


def agregar_contacto(usuario_id, nombre, telefono=None, correo=None):
    """
    US 16 - Agregar contacto de emergencia.

    Criterios:
    - Cada estudiante puede tener hasta 2 contactos
    - Valida formato de telefono y correo
    """
    # Validar limite de 2 contactos
    existentes = ejecutar_query(
        "SELECT COUNT(*) AS total FROM contactos_emergencia WHERE usuario_id = %s",
        (usuario_id,),
        fetch=True
    )
    if existentes and existentes[0]['total'] >= 2:
        return {'ok': False, 'mensaje': 'Maximo 2 contactos de emergencia permitidos'}

    # Validar que al menos haya telefono o correo
    if not telefono and not correo:
        return {'ok': False, 'mensaje': 'Debes proporcionar telefono o correo'}

    # Validar formato del telefono si viene
    if telefono and not validar_telefono(telefono):
        return {'ok': False, 'mensaje': 'Formato de telefono invalido'}

    nuevo_id = ejecutar_query(
        """INSERT INTO contactos_emergencia (usuario_id, nombre, telefono, correo)
           VALUES (%s, %s, %s, %s)""",
        (usuario_id, nombre, telefono, correo),
        fetch=False
    )

    return {
        'ok': True,
        'mensaje': 'Contacto agregado',
        'id': nuevo_id
    }


def listar_contactos(usuario_id):
    """Lista los contactos de emergencia de un estudiante."""
    return ejecutar_query(
        """SELECT id, nombre, telefono, correo
           FROM contactos_emergencia WHERE usuario_id = %s""",
        (usuario_id,),
        fetch=True
    ) or []


def eliminar_contacto(contacto_id, usuario_id):
    """Elimina un contacto (solo el dueno puede)."""
    filas = ejecutar_query(
        "DELETE FROM contactos_emergencia WHERE id = %s AND usuario_id = %s",
        (contacto_id, usuario_id),
        fetch=False
    )
    if filas and filas > 0:
        return {'ok': True, 'mensaje': 'Contacto eliminado'}
    return {'ok': False, 'mensaje': 'Contacto no encontrado'}
