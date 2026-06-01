"""
insert.py - Insercion de usuarios SafeCampus UCB
Para uso administrativo (alta de monitores, estudiantes desde panel admin)
"""

from conexion import ejecutar_query
from seguridad import hashear_password, validar_correo_ucb


def insertar_usuario(correo, password, nombre, telefono=None, rol='estudiante'):
    """
    Insercion administrativa de un usuario.

    A diferencia de registrar_usuario(), este metodo crea la cuenta
    YA VERIFICADA (lo usa el admin desde el panel).

    Args:
        correo: correo @ucb.edu.bo
        password: password en texto plano (se hashea internamente)
        nombre: nombre completo
        telefono: opcional
        rol: 'estudiante' | 'monitor' | 'admin'

    Returns:
        dict con {ok: bool, mensaje: str, id: int|None}
    """
    # Validar dominio
    if not validar_correo_ucb(correo):
        return {
            'ok': False,
            'mensaje': 'Solo se permiten correos @ucb.edu.bo',
            'id': None
        }

    # Validar rol
    if rol not in ('estudiante', 'monitor', 'admin'):
        return {
            'ok': False,
            'mensaje': 'Rol invalido',
            'id': None
        }

    # Verificar duplicados
    existentes = ejecutar_query(
        "SELECT id FROM usuarios WHERE correo = %s",
        (correo,),
        fetch=True
    )
    if existentes:
        return {
            'ok': False,
            'mensaje': 'El correo ya esta registrado',
            'id': None
        }

    # Hashear password
    password_hash = hashear_password(password)

    # Insertar (cuenta verificada por defecto - alta administrativa)
    query = """
        INSERT INTO usuarios
            (correo, password_hash, nombre, telefono, rol, is_verified, estado)
        VALUES (%s, %s, %s, %s, %s, TRUE, 'activo')
    """
    nuevo_id = ejecutar_query(
        query,
        (correo, password_hash, nombre, telefono, rol),
        fetch=False
    )

    if nuevo_id:
        return {
            'ok': True,
            'mensaje': f'Usuario {correo} insertado correctamente',
            'id': nuevo_id
        }

    return {'ok': False, 'mensaje': 'Error al insertar', 'id': None}


if __name__ == "__main__":
    resultado = insertar_usuario(
        'test.usuario@ucb.edu.bo',
        'test1234',
        'Usuario de Prueba',
        '70999999',
        'estudiante'
    )
    print(resultado)
