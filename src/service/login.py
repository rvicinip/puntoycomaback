'''
   login

   Realiza las verificaciones y tareas necesarias para garantizar el acceso sólo a los usuarios registrados en el sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src.service import privated
from flask import jsonify, request
import jwt
import datetime
from src import app
from src.model import user

@app.route('/')
def inicio():
    '''
       inicio: Busca todos los usuario de una empresa en la coleeción de usaurio \n
    '''
    print("In inicio")
    ## resp = usuario.getUsersByCompany('1asdc23')
    return jsonify({"inicio": "Servidor iniciado", 'data': 'resp'})

@app.route('/access', methods = ['POST'])
def login():
   '''
      login: realiza las validaciones de usuario para permitir o no el ingreso a la aplicacion
   '''
   data = request.json
   print("In login")
   if 'id_usuario' in data and 'clave' in data:
      ingreso = user.validatePassword(data)
      if ingreso['response'] == 'ERROR':
        return jsonify(ingreso)
      usuario = ingreso['data']
      token = jwt.encode({'user' : usuario['id_usuario'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=5)}, app.config['SECRET_KEY'])
      return jsonify({'response': 'OK', 'data': usuario, 'token': token})
   return jsonify({'response': 'ERROR', 'message': 'Usuario y Contraseña son requeridos'})

@app.route('/exit', methods = ['POST', 'GET'])
@privated
def logout(usuario):
    '''
       logout: Cierra la sesión de un usuario \n
    '''
    print("In logout", usuario)
    return jsonify({'response': 'OK', 'message': 'Sesión terminada'})
