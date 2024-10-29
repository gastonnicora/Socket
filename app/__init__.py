from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

from os import path, environ

from app.socketio import socketio
from app.redis import run_redis_subscriber

def create_app(environment="development"):
 
    # Configuración inicial de la app   
    app = Flask(__name__)
    app.jinja_env.line_statement_prefix = '#'
    app.config['SECRET_KEY']= environ.get("SECRET_KEY","1234")

    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    env = environ.get("FLASK_ENV", environment)
    socketio.init_app(app)
    
    run_redis_subscriber()
    return app 
