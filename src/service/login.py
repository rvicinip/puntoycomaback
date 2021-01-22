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
from src.mongoCRUD import connector
from config import MONGO, DB

@app.route('/')
def inicio():
    '''
       :getUsers: Busca todos los usuario de una empresa en la coleeción de usaurio
       :params: idCompany: Id de la empresa a la que está asociado el usuario en la DB 
    '''
    print("In inicio")
    coleccion = request.json['coleccion']
    idMongo = request.json['_id']
    resultado = connector.getCollectionById(MONGO, DB, coleccion, idMongo)
    return jsonify({"inicio": "Servidor iniciado", "data": resultado})

@app.route('/access', methods = ['POST'])
def login():
    '''
       :getUsers: Busca todos los usuario de una empresa en la coleeción de usaurio
       :params: idCompany: Id de la empresa a la que está asociado el usuario en la DB 
    '''
    usuario = request.json['id_usuario']
    clave = request.json['clave']
    print("In login:", usuario)
    ingreso = user.getUserByUsuario(usuario)
    if ingreso == None:
      return {"response": "ERROR", "message": "Usuario no registrado"}
    else:
      if clave == ingreso['clave']:
        session['usuario'] = usuario
        return ingreso
      else:
        return {"response": "ERROR", "message": "Contraseña errada"}

@app.route('/exit', methods = ['POST', 'GET'])
def logout():
    '''
       :getUsers: Busca todos los usuario de una empresa en la coleeción de usaurio
       :params: idCompany: Id de la empresa a la que está asociado el usuario en la DB 
    '''
    print("In logout")
    session.clear()
    return "Chao"
