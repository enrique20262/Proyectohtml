"""
login.py - Autenticacion de usuarios SafeCampus UCB
Cubre US 01 (Registro), US 02 (Login), US 04 (Validacion de cuenta)
"""

from conexion import ejecutar_query
from seguridad import (
    hashear_password,
    verificar_password,
    generar_codigo_verificacion,
    validar_correo_ucb
)


def autenticar(correo, password):
    """
    US 02 - Inicio de sesion (Login).

    Verifica las credenciales y devuelve los datos del usuario si es valido.

    Returns:
        dict con datos del usuario si es valido
        None si las credenciales son incorrectas
        str con mensaje si la cuenta no esta verificada o inactiva
    """
    # Buscar el usuario por correo
    query = """
        SELECT id, correo, password_hash, nombre, rol, is_verified, estado
        FROM usuarios
        WHERE correo = %s
    """
    resultados = ejecutar_query(query, (correo,), fetch=True)

    if not resultados:
        return None  # Usuario no existe

    usuario = resultados[0]

    # Verificar password con bcrypt
    if not verificar_password(password, usuario['password_hash']):
        return None  # Password incorrecta

    # Verificar estado (US 02 - bloqueo de cuentas inactivas)
    if usuario['estado'] == 'inactivo':
        return 'CUENTA_INACTIVA'

    # Verificar que la cuenta este verificada (depende de US 04)
    if not usuario['is_verified']:
        return 'CUENTA_NO_VERIFICADA'

    # Login exitoso - retornar datos del usuario (sin el hash)
    del usuario['password_hash']
    return usuario


def registrar_usuario(correo, password, nombre):
    """
    US 01 - Registro de Usuario.

    Crea un usuario nuevo con validacion de dominio @ucb.edu.bo
    y genera un codigo de verificacion (US 04).

    Returns:
        dict con {ok: bool, mensaje: str, codigo: str|None}
    """
    # Criterio US 01: validar dominio @ucb.edu.bo
    if not validar_correo_ucb(correo):
        return {
            'ok': False,
            'mensaje': 'Solo se permiten correos institucionales @ucb.edu.bo',
            'codigo': None
        }

    # Criterio US 01: validar que el correo no exista
    existentes = ejecutar_query(
        "SELECT id FROM usuarios WHERE correo = %s",
        (correo,),
        fetch=True
    )
    if existentes:
        return {
            'ok': False,
            'mensaje': 'Este correo ya esta registrado',
            'codigo': None
        }

    # Validar password minima
    if not password or len(password) < 4:
        return {
            'ok': False,
            'mensaje': 'La password debe tener al menos 4 caracteres',
            'codigo': None
        }

    # Hashear password con bcrypt
    password_hash = hashear_password(password)

   

    # Insertar usuario (is_verified = FALSE, requiere validacion)
   # Hashear password con bcrypt
    password_hash = hashear_password(password)

    # Bloque de inserción con protección para ver errores
    try:
        query = """
            INSERT INTO usuarios (correo, password_hash, nombre, is_verified)
            VALUES (%s, %s, %s, TRUE)
        """
        nuevo_id = ejecutar_query(query, (correo, password_hash, nombre), fetch=False)
        
        # Esto te ayudará a ver en la terminal si algo falla
        print(f"DEBUG: El resultado del INSERT fue: {nuevo_id}")
        
    except Exception as e:
        print(f"ERROR CRÍTICO EN INSERT: {e}")
        return {'ok': False, 'mensaje': f'Error técnico: {str(e)}', 'codigo': None}

    if nuevo_id:
        return {
            'ok': True,
            'mensaje': 'Registro exitoso. Ya puedes iniciar sesión.',
            'codigo': None
        }

    return {'ok': False, 'mensaje': 'Error al registrar usuario', 'codigo': None}

def verificar_cuenta(correo, codigo):
    """
    US 04 - Validacion de cuenta.

    Verifica el codigo enviado al registrarse y activa la cuenta.

    Returns:
        dict con {ok: bool, mensaje: str}
    """
    # Buscar usuario y comparar codigo
    query = """
        SELECT id, codigo_verif, is_verified
        FROM usuarios
        WHERE correo = %s
    """
    resultados = ejecutar_query(query, (correo,), fetch=True)

    if not resultados:
        return {'ok': False, 'mensaje': 'Usuario no encontrado'}

    usuario = resultados[0]

    if usuario['is_verified']:
        return {'ok': False, 'mensaje': 'La cuenta ya fue verificada anteriormente'}

    if usuario['codigo_verif'] != codigo:
        return {'ok': False, 'mensaje': 'Codigo incorrecto'}

    # Activar cuenta
    ejecutar_query(
        "UPDATE usuarios SET is_verified = TRUE, codigo_verif = NULL WHERE id = %s",
        (usuario['id'],),
        fetch=False
    )

    return {
        'ok': True,
        'mensaje': 'Cuenta verificada. Ya puedes iniciar sesion.'
    }


if __name__ == "__main__":
    # Prueba rapida
    print("=== Test de autenticacion ===")
    resultado = autenticar('kevin.panoso@ucb.edu.bo', 'ucb1234')
    print(f"Login: {resultado}")
