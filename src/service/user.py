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
from flask import jsonify, request, session

@app.route('/user/<company>', methods = ['POST'])
def createUser(company):
    '''
       :createUser: Crea un usuario de una empresa en la coleeción de usaurio
       :params: company: Contiene el identificador de la empresa
    '''
    print("In createUser:", company)
    dato = request.json
    usuario = user.addUser(dato, company)
    return jsonify({'response': usuario})

@app.route('/users/<company>', methods = ['GET'])
def obtainUsers(company):
    '''
       :obtainUsers: Optiene los usuarios de una empresa en la coleeción de usaurio
       :params: company: Contiene el identificador de la empresa
    '''
    print("In obtainUsers:", company)
    usuario = user.getUsersByCompany(company)
    return jsonify({'response': usuario})

@app.route('/users', methods = ['POST'])
def obtaineUsers():
    session.clear()
 