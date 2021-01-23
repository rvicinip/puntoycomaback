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
from src.model import user


@app.route('/')
def inicio():
    '''
       getUsers: Busca todos los usuario de una empresa en la coleeción de usaurio \n
       @params: 
         idCompany: Id de la empresa a la que está asociado el usuario en la DB 
    '''
    print("In inicio")
    idMongo = request.json['_id']
    resultado = user.getUserById(idMongo)
    return jsonify({"inicio": "Servidor iniciado", "data": resultado})

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
      else:
        session['usuario'] = usuario
        return jsonify(ingreso)
    else:
      return jsonify({'response': 'ERROR', 'message': 'Usuario y Contraseña son requeridos'})

@app.route('/exit', methods = ['POST', 'GET'])
def logout():
    '''
       getUsers: Busca todos los usuario de una empresa en la coleeción de usaurio \n
       @params: 
         idCompany: Id de la empresa a la que está asociado el usuario en la DB 
    '''
    print("In logout")
    session.clear()
    return jsonify({'response': 'OK', 'message': 'Sesión terminada'})
