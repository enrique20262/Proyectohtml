"""
main.py - Menu interactivo CLI de SafeCampus UCB
Permite probar todas las funcionalidades desde la terminal.

Ejecutar: python main.py
"""

import os
import sys
from login import autenticar, registrar_usuario, verificar_cuenta
from insert import insertar_usuario
from update import actualizar_perfil
from delete import desactivar_usuario, reactivar_usuario
from list import listar_usuarios, obtener_usuario_por_id
from ubicaciones import registrar_ubicacion, obtener_usuarios_cercanos, obtener_ubicacion_actual
from alertas import (
    emitir_alerta, listar_alertas_activas,
    marcar_alerta_atendida, listar_historial_alertas
)
from contactos import agregar_contacto, listar_contactos
from reportes import (
    reporte_usuarios_por_estado,
    reporte_usuarios_por_rol,
    reporte_alertas_por_estado,
    reporte_zonas_riesgo
)


# Estado de sesion
USUARIO_ACTUAL = None


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa():
    input("\nPresiona Enter para continuar...")


def header(titulo):
    print("=" * 60)
    print(f"  SafeCampus UCB  -  {titulo}")
    print("=" * 60)


# ============================================================
# AUTENTICACION
# ============================================================

def pantalla_login():
    global USUARIO_ACTUAL
    limpiar_pantalla()
    header("Iniciar Sesion")

    correo = input("Correo @ucb.edu.bo: ").strip()
    password = input("Password: ").strip()

    resultado = autenticar(correo, password)

    if resultado is None:
        print("\n[ERROR] Credenciales incorrectas")
    elif resultado == 'CUENTA_NO_VERIFICADA':
        print("\n[ERROR] Debes verificar tu cuenta primero")
    elif resultado == 'CUENTA_INACTIVA':
        print("\n[ERROR] Tu cuenta esta desactivada")
    else:
        USUARIO_ACTUAL = resultado
        print(f"\n[OK] Bienvenido {resultado['nombre']} ({resultado['rol']})")

    pausa()


def pantalla_registro():
    limpiar_pantalla()
    header("Registro de Usuario")

    correo = input("Correo @ucb.edu.bo: ").strip()
    password = input("Password (min 4 caracteres): ").strip()
    nombre = input("Nombre completo: ").strip()

    resultado = registrar_usuario(correo, password, nombre)
    print(f"\n{resultado['mensaje']}")
    if resultado['ok']:
        print(f"\n[CODIGO DE VERIFICACION] {resultado['codigo']}")
        print("Anota este codigo para activar tu cuenta (US 04)")

    pausa()


def pantalla_verificar():
    limpiar_pantalla()
    header("Verificar Cuenta")

    correo = input("Correo: ").strip()
    codigo = input("Codigo de verificacion: ").strip()

    resultado = verificar_cuenta(correo, codigo)
    print(f"\n{resultado['mensaje']}")
    pausa()


# ============================================================
# PERFIL Y USUARIOS
# ============================================================

def pantalla_listar_usuarios():
    limpiar_pantalla()
    header("Listado de Usuarios")

    usuarios = listar_usuarios()
    print(f"\nTotal: {len(usuarios)} usuarios\n")
    print(f"{'ID':<4}{'Correo':<35}{'Nombre':<25}{'Rol':<12}{'Estado':<10}")
    print("-" * 86)
    for u in usuarios:
        print(f"{u['id']:<4}{u['correo']:<35}{u['nombre']:<25}{u['rol']:<12}{u['estado']:<10}")

    pausa()


def pantalla_editar_perfil():
    if not USUARIO_ACTUAL:
        print("\nDebes iniciar sesion primero")
        pausa()
        return

    limpiar_pantalla()
    header(f"Editar Perfil - {USUARIO_ACTUAL['nombre']}")

    nombre = input("Nuevo nombre (Enter para no cambiar): ").strip() or None
    telefono = input("Nuevo telefono (Enter para no cambiar): ").strip() or None

    resultado = actualizar_perfil(USUARIO_ACTUAL['id'], nombre=nombre, telefono=telefono)
    print(f"\n{resultado['mensaje']}")
    pausa()


def pantalla_desactivar():
    limpiar_pantalla()
    header("Desactivar Usuario (baja logica)")

    try:
        id_usuario = int(input("ID del usuario a desactivar: "))
        resultado = desactivar_usuario(id_usuario)
        print(f"\n{resultado['mensaje']}")
    except ValueError:
        print("ID invalido")

    pausa()


# ============================================================
# UBICACIONES Y MAPA
# ============================================================

def pantalla_enviar_ubicacion():
    if not USUARIO_ACTUAL:
        print("\nDebes iniciar sesion primero")
        pausa()
        return

    limpiar_pantalla()
    header("Enviar mi Ubicacion (US 08)")

    print("Demo: usando coordenadas del campus UCB Santa Cruz")
    print("Latitud: -17.7833, Longitud: -63.1821")
    print()
    usar_demo = input("Usar estas coordenadas? (s/n): ").strip().lower()

    if usar_demo == 's':
        lat, lng = -17.7833, -63.1821
    else:
        try:
            lat = float(input("Latitud: "))
            lng = float(input("Longitud: "))
        except ValueError:
            print("Coordenadas invalidas")
            pausa()
            return

    resultado = registrar_ubicacion(USUARIO_ACTUAL['id'], lat, lng)
    print(f"\n{resultado['mensaje']}")
    pausa()


def pantalla_ver_cercanos():
    if not USUARIO_ACTUAL:
        print("\nDebes iniciar sesion primero")
        pausa()
        return

    limpiar_pantalla()
    header("Usuarios Cercanos (US 09)")

    cercanos = obtener_usuarios_cercanos(USUARIO_ACTUAL['id'], radio_metros=500)
    print(f"\nUsuarios anonimos dentro de 500m: {len(cercanos)}\n")

    if cercanos:
        print(f"{'#':<4}{'Latitud':<15}{'Longitud':<15}{'Distancia':<12}")
        print("-" * 46)
        for i, c in enumerate(cercanos, 1):
            print(f"{i:<4}{c['latitud']:<15}{c['longitud']:<15}{c['distancia_metros']}m")
        print("\n[Nota US 09] No se muestra ID ni nombre por privacidad")
    else:
        print("No hay estudiantes registrados cerca")

    pausa()


# ============================================================
# BOTON DE PANICO Y MONITOREO (CORE)
# ============================================================

def pantalla_boton_panico():
    if not USUARIO_ACTUAL:
        print("\nDebes iniciar sesion primero")
        pausa()
        return

    limpiar_pantalla()
    print("=" * 60)
    print("           !!!  BOTON DE PANICO SOS  !!!")
    print("=" * 60)
    print("\nAl activar la alerta, el centro de monitoreo UCB sera")
    print("notificado con tu ubicacion exacta.\n")

    confirmar = input("Confirmar emision de alerta? (SI/no): ").strip().upper()
    if confirmar != 'SI':
        print("Alerta cancelada")
        pausa()
        return

    # Usar ultima ubicacion conocida o pedirla
    ubicacion = obtener_ubicacion_actual(USUARIO_ACTUAL['id'])
    if ubicacion:
        lat, lng = ubicacion['latitud'], ubicacion['longitud']
        print(f"\nUsando tu ultima ubicacion: ({lat}, {lng})")
    else:
        lat, lng = -17.7833, -63.1821  # default campus UCB
        print(f"\nNo hay ubicacion previa, usando ubicacion del campus")

    resultado = emitir_alerta(USUARIO_ACTUAL['id'], lat, lng)
    print(f"\n*** {resultado['mensaje']} ***")
    pausa()


def pantalla_panel_monitoreo():
    if not USUARIO_ACTUAL:
        print("\nDebes iniciar sesion primero")
        pausa()
        return

    if USUARIO_ACTUAL['rol'] not in ('monitor', 'admin'):
        print("\nSolo monitores pueden acceder al panel")
        pausa()
        return

    limpiar_pantalla()
    header("PANEL DE MONITOREO UCB (US 13)")

    activas = listar_alertas_activas()
    print(f"\n*** {len(activas)} ALERTAS ACTIVAS ***\n")

    if not activas:
        print("No hay alertas activas en este momento.")
    else:
        print(f"{'ID':<5}{'Estudiante':<25}{'Ubicacion':<30}{'Hace':<10}")
        print("-" * 70)
        for a in activas:
            ubic = f"({a['latitud']}, {a['longitud']})"
            tiempo = f"{a['minutos_transcurridos']} min"
            print(f"{a['alerta_id']:<5}{a['nombre_estudiante']:<25}{ubic:<30}{tiempo:<10}")

        print()
        marcar = input("ID de alerta a atender (Enter para volver): ").strip()
        if marcar:
            try:
                resultado = marcar_alerta_atendida(int(marcar), USUARIO_ACTUAL['id'])
                print(f"\n{resultado['mensaje']}")
            except ValueError:
                print("ID invalido")

    pausa()


# ============================================================
# CONTACTOS Y REPORTES
# ============================================================

def pantalla_contactos():
    if not USUARIO_ACTUAL:
        print("\nDebes iniciar sesion primero")
        pausa()
        return

    limpiar_pantalla()
    header(f"Contactos de Emergencia - {USUARIO_ACTUAL['nombre']}")

    contactos = listar_contactos(USUARIO_ACTUAL['id'])
    print(f"\nTienes {len(contactos)} contacto(s) registrado(s):")
    for c in contactos:
        print(f"  - {c['nombre']} | Tel: {c['telefono']} | Email: {c['correo']}")

    if len(contactos) < 2:
        print("\nPuedes agregar uno mas. Presiona Enter para saltar.")
        nombre = input("\nNombre del contacto: ").strip()
        if nombre:
            telefono = input("Telefono: ").strip() or None
            correo = input("Correo: ").strip() or None
            resultado = agregar_contacto(USUARIO_ACTUAL['id'], nombre, telefono, correo)
            print(f"\n{resultado['mensaje']}")

    pausa()


def pantalla_reportes():
    limpiar_pantalla()
    header("Reportes y Estadisticas")

    print("\n[1] Usuarios por estado:")
    for r in reporte_usuarios_por_estado():
        print(f"    {r['estado']}: {r['total']}")

    print("\n[2] Usuarios por rol:")
    for r in reporte_usuarios_por_rol():
        print(f"    {r['rol']}: {r['total']}")

    print("\n[3] Alertas por estado:")
    for r in reporte_alertas_por_estado():
        print(f"    {r['estado']}: {r['total']}")

    print("\n[4] Zonas de riesgo (mas alertas):")
    zonas = reporte_zonas_riesgo()
    if zonas:
        for z in zonas:
            print(f"    ({z['lat_aprox']}, {z['lng_aprox']}) -> {z['total_alertas']} alertas")
    else:
        print("    Sin datos suficientes")

    pausa()


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu_principal():
    while True:
        limpiar_pantalla()
        header("SafeCampus UCB - Equipo SCHEIBE")

        if USUARIO_ACTUAL:
            print(f"\nSesion activa: {USUARIO_ACTUAL['nombre']} ({USUARIO_ACTUAL['rol']})\n")
        else:
            print("\nSin sesion activa\n")

        print("--- ACCESO ---")
        print("  1) Registrarme (US 01)")
        print("  2) Verificar cuenta (US 04)")
        print("  3) Iniciar sesion (US 02)")
        print("  4) Cerrar sesion")
        print()
        print("--- PERFIL ---")
        print("  5) Listar usuarios")
        print("  6) Editar mi perfil (US 05)")
        print("  7) Mis contactos de emergencia (US 16)")
        print()
        print("--- UBICACION Y MAPA ---")
        print("  8) Enviar mi ubicacion (US 08)")
        print("  9) Ver usuarios cercanos (US 09)")
        print()
        print("--- SOS Y MONITOREO ---")
        print(" 10) *** BOTON DE PANICO *** (US 11/12)")
        print(" 11) Panel de Monitoreo (US 13) [solo monitor]")
        print()
        print("--- ADMIN ---")
        print(" 12) Desactivar usuario")
        print(" 13) Reportes y estadisticas")
        print()
        print("  0) Salir")

        opcion = input("\nOpcion: ").strip()

        if opcion == '1':   pantalla_registro()
        elif opcion == '2': pantalla_verificar()
        elif opcion == '3': pantalla_login()
        elif opcion == '4':
            globals()['USUARIO_ACTUAL'] = None
            print("Sesion cerrada"); pausa()
        elif opcion == '5': pantalla_listar_usuarios()
        elif opcion == '6': pantalla_editar_perfil()
        elif opcion == '7': pantalla_contactos()
        elif opcion == '8': pantalla_enviar_ubicacion()
        elif opcion == '9': pantalla_ver_cercanos()
        elif opcion == '10': pantalla_boton_panico()
        elif opcion == '11': pantalla_panel_monitoreo()
        elif opcion == '12': pantalla_desactivar()
        elif opcion == '13': pantalla_reportes()
        elif opcion == '0':
            print("\nGracias por usar SafeCampus UCB")
            sys.exit(0)
        else:
            print("Opcion invalida"); pausa()


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nHasta luego")
        sys.exit(0)
