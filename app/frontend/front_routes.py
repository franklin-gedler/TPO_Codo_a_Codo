from flask import Blueprint, render_template, send_from_directory, redirect, url_for

frontend_bp = Blueprint('frontend', __name__)

# Ruta para servir archivos estáticos
@frontend_bp.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend/static', filename)

@frontend_bp.route('/')
def redirigir_a_inicio():
    return redirect(url_for('frontend.index'))

@frontend_bp.route('/inicio')
def index():
    return render_template('inicio.html', title='Página de Inicio')

@frontend_bp.route('/peliculas')
def peliculas():
    return render_template('peliculas.html', title='Peliculas')

@frontend_bp.route('/series')
def series():
    return render_template('series.html', title='Series')

@frontend_bp.route('/contactanos')
def contactanos():
    return render_template('contactanos.html', title='Contactanos')
