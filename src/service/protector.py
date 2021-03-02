'''
protector:
   Decorador para asegurar las rutas del backend garantizando las seguridad de la información al acceso de las mismas

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from flask import request, jsonify
from functools import wraps
from src import app
from src.model import user
import jwt
import traceback

def privated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("In decorated")
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'response': 'ERROR','message' : 'No se recibió el Token'}), 402
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            usuario = user.getUserByUsuario(data['user'])
            if usuario['response'] == 'ERROR':
                return jsonify({'response': 'ERROR', 'message': 'El usuario no está registrado en el sistema'})
        except Exception:
            traceback.print_exc()
            return jsonify({'response': 'ERROR','message' : 'Token no válido'}), 401
        return f(usuario['data'], *args, **kwargs)
    return decorated
