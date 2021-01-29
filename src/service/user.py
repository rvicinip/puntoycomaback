'''
   user

   Realiza todas las transacciones y tareas necesarias para mantener los datos de los usuarios en el sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src import app
from src.model import user
from flask import jsonify, request

@app.route('/user', methods = ['POST'])
def createUser():
    '''
       createUser: Crea un usuario de una empresa en la coleeción de usaurio \n
       @params: 
         company: Contiene el identificador de la empresa
    '''
    print("In createUser")
    dato = request.json
    usuario = user.addUser(dato, company)
    return jsonify(usuario)

@app.route('/users/<company>', methods = ['GET'])
def obtainUsers(company):
    '''
       obtainUsers: Obtiene los usuarios de una empresa en la colección de usaurio \n
       @params: 
         company: Contiene el id mongo de la empresa
    '''
    print("In obtainUsers:", company)
    usuario = user.getUsersByCompany(company)
    return jsonify(usuario)
