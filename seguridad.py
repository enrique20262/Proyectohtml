"""
seguridad.py - Hashing seguro de contrasenas con bcrypt
Equipo SCHEIBE - Sprint 3

NOTA: Se uso bcrypt en lugar de MD5 porque MD5 esta criptograficamente
roto desde 2004. Para un sistema de seguridad estudiantil es indispensable
usar un algoritmo moderno resistente a fuerza bruta y rainbow tables.
"""

import bcrypt
import random
import string
import re


def hashear_password(password_plano):
    """
    Convierte una password en texto plano a un hash seguro con bcrypt.

    Args:
        password_plano: string con la password

    Returns:
        string con el hash (incluye el salt)
    """
    password_bytes = password_plano.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hash_bytes = bcrypt.hashpw(password_bytes, salt)
    return hash_bytes.decode('utf-8')


def verificar_password(password_plano, hash_almacenado):
    """
    Verifica si una password coincide con su hash almacenado.

    Args:
        password_plano: lo que el usuario escribio
        hash_almacenado: lo que esta en la base de datos

    Returns:
        True si coincide, False si no
    """
    try:
        password_bytes = password_plano.encode('utf-8')
        hash_bytes = hash_almacenado.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception:
        return False


def generar_codigo_verificacion():
    """
    Genera un codigo aleatorio de 6 digitos para verificacion (US 04).
    """
    return ''.join(random.choices(string.digits, k=6))


def validar_correo_ucb(correo):
    """
    Valida que el correo tenga el dominio @ucb.edu.bo (US 01).
    """
    patron = r'^[a-zA-Z0-9._%+-]+@ucb\.edu\.bo$'
    return re.match(patron, correo) is not None


def validar_telefono(telefono):
    """
    Valida que el telefono tenga formato numerico valido (US 05, US 16).
    Acepta 7-15 digitos, opcionalmente con + al inicio.
    """
    if not telefono:
        return False
    patron = r'^\+?[0-9]{7,15}$'
    return re.match(patron, telefono) is not None


if __name__ == "__main__":
    # Pruebas rapidas
    print("=== Pruebas de seguridad ===")

    pwd = "ucb1234"
    hash_pwd = hashear_password(pwd)
    print(f"Hash generado: {hash_pwd}")
    print(f"Verificacion correcta: {verificar_password(pwd, hash_pwd)}")
    print(f"Verificacion incorrecta: {verificar_password('otraPass', hash_pwd)}")

    print(f"\nCodigo de verificacion: {generar_codigo_verificacion()}")

    print(f"\nCorreo valido UCB: {validar_correo_ucb('kevin@ucb.edu.bo')}")
    print(f"Correo invalido: {validar_correo_ucb('kevin@gmail.com')}")

    print(f"\nTelefono valido: {validar_telefono('70123456')}")
    print(f"Telefono invalido: {validar_telefono('abc123')}")
