"""
update.py - Actualizacion de datos de usuario
Cubre US 05 (Edicion de perfil)
"""

from conexion import ejecutar_query
from seguridad import validar_telefono, hashear_password


def actualizar_perfil(usuario_id, nombre=None, telefono=None):
    """
    US 05 - Edicion de perfil.

    Permite actualizar nombre y/o telefono de un usuario.

    Criterios de aceptacion:
    - El usuario puede modificar su nombre y numero de contacto.
    - Los cambios deben guardarse en la base de datos tras confirmar.
    - Se valida que el numero de telefono sea un formato numerico valido.

    Args:
        usuario_id: ID del usuario a actualizar
        nombre: nuevo nombre (opcional)
        telefono: nuevo telefono (opcional, se valida formato)

    Returns:
        dict con {ok: bool, mensaje: str}
    """
    # Validar que al menos un campo venga
    if not nombre and not telefono:
        return {
            'ok': False,
            'mensaje': 'Debes enviar al menos un campo a modificar'
        }

    # Validar nombre si viene
    if nombre is not None:
        nombre = nombre.strip()
        if len(nombre) < 2:
            return {
                'ok': False,
                'mensaje': 'El nombre debe tener al menos 2 caracteres'
            }
        if len(nombre) > 100:
            return {
                'ok': False,
                'mensaje': 'El nombre no puede superar 100 caracteres'
            }

    # Criterio US 05: validar formato del telefono
    if telefono is not None and telefono != '':
        if not validar_telefono(telefono):
            return {
                'ok': False,
                'mensaje': 'El telefono debe contener solo digitos (7-15) y opcionalmente + al inicio'
            }

    # Construir query dinamica solo con los campos que vienen
    campos = []
    valores = []

    if nombre:
        campos.append('nombre = %s')
        valores.append(nombre)

    if telefono is not None and telefono != '':
        campos.append('telefono = %s')
        valores.append(telefono)

    valores.append(usuario_id)

    query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = %s"
    filas = ejecutar_query(query, tuple(valores), fetch=False)

    if filas and filas > 0:
        return {
            'ok': True,
            'mensaje': 'Perfil actualizado correctamente'
        }

    return {'ok': False, 'mensaje': 'No se pudo actualizar (usuario no encontrado)'}


def cambiar_password(usuario_id, password_nueva):
    """
    Cambia la password de un usuario (uso interno o admin).
    """
    if len(password_nueva) < 4:
        return {'ok': False, 'mensaje': 'Password muy corta'}

    nuevo_hash = hashear_password(password_nueva)
    ejecutar_query(
        "UPDATE usuarios SET password_hash = %s WHERE id = %s",
        (nuevo_hash, usuario_id),
        fetch=False
    )
    return {'ok': True, 'mensaje': 'Password actualizada'}


if __name__ == "__main__":
    resultado = actualizar_perfil(1, telefono='70111222')
    print(resultado)
