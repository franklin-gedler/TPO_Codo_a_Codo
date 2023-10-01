from flask import render_template, send_from_directory, url_for
from app import app

# Ruta para servir archivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/')
@app.route('/inicio')
def index():
    return render_template('inicio.html', title='Página de Inicio')

@app.route('/peliculas')
def peliculas():
    return render_template('peliculas.html', title='Peliculas')

@app.route('/series')
def series():
    return render_template('series.html', title='Series')

@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html', title='Contactanos')