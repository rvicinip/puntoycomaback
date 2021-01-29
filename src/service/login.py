'''
   login

   Realiza las verificaciones y tareas necesarias para garantizar el acceso sólo a los usuarios registrados en el sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from flask import jsonify, request, session
from src import app
from src.service import user
from src.model import user as usuario
@app.route('/')
def inicio():
    '''
       getUsers: Busca todos los usuario de una empresa en la coleeción de usaurio \n
       @params: 
         idCompany: Id de la empresa a la que está asociado el usuario en la DB 
    '''
    print("In inicio")
    resp = usuario.getUsersByCompany('1asdc23')
    return jsonify({"inicio": "Servidor iniciado", 'data': resp})

@app.route('/access', methods = ['POST'])
def login():
    '''
       login: realiza las validaciones de usuario para permitir o no el ingreso a la aplicacion
    '''
    usuario = request.json['id_usuario']
    clave = request.json['clave']
    print("In login:", usuario)
    if usuario and clave:
      ingreso = user.validatePassword(usuario)
      if ingreso['response'] == 'ERROR':
        return jsonify(ingreso)
      session['usuario'] = usuario
      return jsonify(ingreso)
    return jsonify({'response': 'ERROR', 'message': 'Usuario y Contraseña son requeridos'})

@app.route('/exit', methods = ['POST', 'GET'])
def logout():
    '''
       logout: Cierra la sesión de un usuario \n
    '''
    print("In logout")
    session.clear()
    return jsonify({'response': 'OK', 'message': 'Sesión terminada'})
