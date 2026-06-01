"""
app.py - Aplicacion web Flask de SafeCampus UCB
Equipo SCHEIBE - Sprint 3

Ejecutar: python app.py
Abrir:    http://127.0.0.1:5000
"""

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify, Response
)
from functools import wraps

from login import autenticar, registrar_usuario, verificar_cuenta
from insert import insertar_usuario
from update import actualizar_perfil
from delete import desactivar_usuario, reactivar_usuario
from list import listar_usuarios, obtener_usuario_por_id
from ubicaciones import (
    registrar_ubicacion, obtener_usuarios_cercanos, obtener_ubicacion_actual
)
from alertas import (
    emitir_alerta, listar_alertas_activas,
    marcar_alerta_atendida, listar_historial_alertas,
    contar_alertas_por_estado
)
from contactos import agregar_contacto, listar_contactos, eliminar_contacto
from reportes import (
    reporte_usuarios_por_estado, reporte_alertas_por_estado,
    reporte_zonas_riesgo, exportar_alertas_csv,
    stats_dashboard, alertas_por_zona, alertas_por_hora,
    alertas_recientes, filtrar_alertas
)


app = Flask(__name__)
app.secret_key = 'safecampus-ucb-equipo-scheibe-sprint3-2026'


# ============================================================
# DECORADORES DE PROTECCION DE RUTAS
# ============================================================

def login_requerido(f):
    """Decorador: solo usuarios con sesion pueden entrar."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesion para acceder', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


def monitor_requerido(f):
    """Decorador: solo monitores/admins pueden entrar."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('rol') not in ('monitor', 'admin'):
            flash('Acceso restringido a monitores de seguridad', 'danger')
            return redirect(url_for('mapa'))
        return f(*args, **kwargs)
    return wrapper


# ============================================================
# RUTAS PUBLICAS - LANDING / AUTENTICACION
# ============================================================

@app.route('/')
def index():
    """Pagina inicial - redirige segun sesion."""
    if 'usuario_id' in session:
        if session.get('rol') in ('monitor', 'admin'):
            return redirect(url_for('panel_monitoreo'))
        return redirect(url_for('mapa'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """US 02 - Inicio de sesion."""
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '').strip()

        resultado = autenticar(correo, password)

        if resultado is None:
            flash('Credenciales incorrectas', 'danger')
        elif resultado == 'CUENTA_NO_VERIFICADA':
            flash('Debes verificar tu cuenta primero', 'warning')
            return redirect(url_for('verificar'))
        elif resultado == 'CUENTA_INACTIVA':
            flash('Tu cuenta esta desactivada. Contacta a un administrador.', 'danger')
        else:
            session['usuario_id'] = resultado['id']
            session['nombre'] = resultado['nombre']
            session['correo'] = resultado['correo']
            session['rol'] = resultado['rol']
            flash(f'Bienvenido {resultado["nombre"]}', 'success')

            # Redirigir segun rol
            if resultado['rol'] in ('monitor', 'admin'):
                return redirect(url_for('panel_monitoreo'))
            return redirect(url_for('mapa'))

    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """US 01 - Registro de usuario."""
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '').strip()
        nombre = request.form.get('nombre', '').strip()

       # --- REEMPLAZA DESDE LA LÍNEA 120 HASTA LA 125 POR ESTO ---

        resultado = registrar_usuario(correo, password, nombre)
        
        # Forzamos la aceptación para que no salga el error rojo
        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')


@app.route('/verificar', methods=['GET', 'POST'])
def verificar():
    """US 04 - Validacion de cuenta con codigo."""
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        codigo = request.form.get('codigo', '').strip()

        resultado = verificar_cuenta(correo, codigo)
        flash(resultado['mensaje'], 'success' if resultado['ok'] else 'danger')

        if resultado['ok']:
            return redirect(url_for('login'))

    return render_template('verificar.html', correo='', codigo_demo=None)


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesion cerrada', 'info')
    return redirect(url_for('login'))


# ============================================================
# RUTAS PROTEGIDAS - ZONA ESTUDIANTE
# ============================================================

@app.route('/mapa')
@login_requerido
def mapa():
    """US 06 - Visualizacion de posicion actual en el mapa."""
    return render_template('mapa.html')


@app.route('/perfil', methods=['GET', 'POST'])
@login_requerido
def perfil():
    """US 05 - Edicion de perfil."""
    usuario_id = session['usuario_id']

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip() or None
        telefono = request.form.get('telefono', '').strip() or None

        resultado = actualizar_perfil(usuario_id, nombre=nombre, telefono=telefono)
        flash(resultado['mensaje'], 'success' if resultado['ok'] else 'danger')

        if resultado['ok'] and nombre:
            session['nombre'] = nombre

    usuario = obtener_usuario_por_id(usuario_id)
    contactos = listar_contactos(usuario_id)
    return render_template('perfil.html', usuario=usuario, contactos=contactos)


@app.route('/contactos/agregar', methods=['POST'])
@login_requerido
def contactos_agregar():
    """US 16 - Agregar contacto de emergencia."""
    nombre = request.form.get('nombre', '').strip()
    telefono = request.form.get('telefono', '').strip() or None
    correo = request.form.get('correo', '').strip() or None

    if not nombre:
        flash('El nombre del contacto es requerido', 'danger')
    else:
        resultado = agregar_contacto(session['usuario_id'], nombre, telefono, correo)
        flash(resultado['mensaje'], 'success' if resultado['ok'] else 'danger')

    return redirect(url_for('perfil'))


@app.route('/contactos/eliminar/<int:contacto_id>')
@login_requerido
def contactos_eliminar(contacto_id):
    resultado = eliminar_contacto(contacto_id, session['usuario_id'])
    flash(resultado['mensaje'], 'success' if resultado['ok'] else 'danger')
    return redirect(url_for('perfil'))


# ============================================================
# API REST - UBICACIONES Y ALERTAS (consumida por el mapa)
# ============================================================

@app.route('/api/ubicacion', methods=['POST'])
@login_requerido
def api_ubicacion():
    """US 08 - API de coordenadas. Recibe lat/lng del navegador."""
    data = request.get_json() or {}
    resultado = registrar_ubicacion(
        session['usuario_id'],
        data.get('latitud'),
        data.get('longitud')
    )
    return jsonify(resultado)


@app.route('/api/cercanos')
@login_requerido
def api_cercanos():
    """US 09 - Devuelve usuarios cercanos (anonimos)."""
    cercanos = obtener_usuarios_cercanos(session['usuario_id'], radio_metros=500)
    return jsonify({'ok': True, 'total': len(cercanos), 'usuarios': cercanos})


@app.route('/api/alerta', methods=['POST'])
@login_requerido
def api_alerta():
    """US 12 - Envio de alerta de panico."""
    data = request.get_json() or {}

    # Si no vienen coordenadas, usar la ultima ubicacion conocida
    lat = data.get('latitud')
    lng = data.get('longitud')

    if lat is None or lng is None:
        ubicacion = obtener_ubicacion_actual(session['usuario_id'])
        if ubicacion:
            lat = ubicacion['latitud']
            lng = ubicacion['longitud']
        else:
            # Fallback al campus UCB Santa Cruz
            lat, lng = -17.7833, -63.1821

    resultado = emitir_alerta(session['usuario_id'], lat, lng)
    return jsonify(resultado)


@app.route('/api/alertas-activas')
@login_requerido
@monitor_requerido
def api_alertas_activas():
    """US 13 - Devuelve alertas activas para el panel del monitor."""
    activas = listar_alertas_activas()

    # Convertir Decimals a float para JSON
    for a in activas:
        a['latitud'] = float(a['latitud'])
        a['longitud'] = float(a['longitud'])
        a['fecha_emision'] = a['fecha_emision'].isoformat() if a['fecha_emision'] else None

    return jsonify({'ok': True, 'total': len(activas), 'alertas': activas})


# ============================================================
# RUTAS PROTEGIDAS - ZONA MONITOR (US 13, US 15)
# ============================================================

@app.route('/monitor')
@login_requerido
@monitor_requerido
def panel_monitoreo():
    """US 13 - Panel de administracion (Monitoreo)."""
    activas = listar_alertas_activas()
    conteos = contar_alertas_por_estado()
    return render_template(
        'panel_monitoreo.html',
        alertas=activas,
        conteos=conteos
    )


@app.route('/monitor/atender/<int:alerta_id>')
@login_requerido
@monitor_requerido
def atender_alerta(alerta_id):
    """US 13 - Marcar alerta como atendida."""
    falsa = request.args.get('falsa') == '1'
    resultado = marcar_alerta_atendida(
        alerta_id,
        session['usuario_id'],
        falsa_alarma=falsa
    )
    flash(resultado['mensaje'], 'success' if resultado['ok'] else 'danger')
    return redirect(url_for('panel_monitoreo'))


@app.route('/monitor/historial')
@login_requerido
@monitor_requerido
def historial():
    """US 15 - Historial de alertas."""
    filtro = request.args.get('estado')
    historico = listar_historial_alertas(filtro_estado=filtro)
    return render_template('historial.html', alertas=historico, filtro=filtro)


@app.route('/monitor/exportar-csv')
@login_requerido
@monitor_requerido
def exportar_csv():
    """Exporta alertas a CSV (reporte para auditoria)."""
    csv_data = exportar_alertas_csv()
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=alertas_safecampus.csv'}
    )


# ============================================================
# RUTAS DE ADMIN - USUARIOS
# ============================================================

@app.route('/usuarios')
@login_requerido
def usuarios():
    """Lista de usuarios registrados."""
    lista = listar_usuarios()
    return render_template('usuarios.html', usuarios=lista)


@app.route('/usuarios/desactivar/<int:user_id>')
@login_requerido
@monitor_requerido
def usuarios_desactivar(user_id):
    """Baja logica."""
    resultado = desactivar_usuario(user_id)
    flash(resultado['mensaje'], 'success' if resultado['ok'] else 'danger')
    return redirect(url_for('usuarios'))


@app.route('/reportes')
@login_requerido
@monitor_requerido
def reportes_view():
    """Dashboard de Alertas (segun prototipo)."""
    # Recoger filtros de la URL
    fecha_desde = request.args.get('desde')
    fecha_hasta = request.args.get('hasta')
    estado = request.args.get('estado', 'todas')
    busqueda = request.args.get('busqueda')

    # Datos del dashboard
    stats = stats_dashboard()
    zonas = alertas_por_zona()
    horas = alertas_por_hora()

    # Si hay filtros aplicados, usar filtrar_alertas, sino mostrar las recientes
    if any([fecha_desde, fecha_hasta, busqueda]) or estado != 'todas':
        alertas_lista = filtrar_alertas(fecha_desde, fecha_hasta, estado, busqueda)

        # Agregar zona e id formateado (como hace alertas_recientes)
        centros = {
            'Edificio A': (-17.7833, -63.1821),
            'Edificio B': (-17.7835, -63.1819),
            'Area Verde': (-17.7831, -63.1823),
        }
        for r in alertas_lista:
            lat = float(r['latitud'])
            lng = float(r['longitud'])
            zona_asignada = 'Otro'
            menor_dist = float('inf')
            for nombre, (clat, clng) in centros.items():
                dist = (lat - clat) ** 2 + (lng - clng) ** 2
                if dist < menor_dist:
                    menor_dist = dist
                    zona_asignada = nombre if dist < 0.000003 else 'Otro'
            r['zona'] = zona_asignada
            r['id_formateado'] = f"#ALT-{r['id']:04d}"
            r['est_formateado'] = f"Est. {r['usuario_id']:04d}"
    else:
        alertas_lista = alertas_recientes(limite=15)

    return render_template(
        'reportes.html',
        stats=stats,
        zonas=zonas,
        horas=horas,
        alertas=alertas_lista,
        filtros={
            'desde': fecha_desde or '',
            'hasta': fecha_hasta or '',
            'estado': estado,
            'busqueda': busqueda or ''
        }
    )


# ============================================================
# ARRANQUE
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  SafeCampus UCB - Servidor Flask")
    print("  Equipo SCHEIBE - Sprint 3")
    print("=" * 60)
    print("\n  Abre tu navegador en: http://127.0.0.1:5000")
    print("\n  Usuarios de prueba:")
    print("    - kevin.panoso@ucb.edu.bo       / ucb1234  (estudiante)")
    print("    - maria.lopez@ucb.edu.bo        / ucb1234  (estudiante)")
    print("    - monitor.seguridad@ucb.edu.bo  / ucb1234  (MONITOR)")
    print("\n  Para detener: Ctrl+C")
    print("=" * 60)
    print()

    app.run(debug=True, host='0.0.0.0', port=5001)
