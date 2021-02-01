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
from src.utility.validator import validateFields
from .protector import privated
from flask import jsonify, request

@app.route('/user', methods = ['POST'])
@privated
def createUser():
   '''
      createUser: Crea un usuario de la empresa en la coleeción de usaurio \n
   '''
   ## Validad que se enviarion todos los campos
   dato = request.json
   campos = ['id_usuario', 'nombre', 'empresa', 'clave']
   valida = validateFields(campos, dato)
   if valida['response'] == 'ERROR':
      return jsonify(valida)
   print("In createUser:", dato['id_usuario'])
   resp = user.addUserEmpresa(dato)
   return jsonify(resp)

@app.route('/users/<company>', methods = ['GET'])
@privated
def obtainUsers(company):
    '''
       obtainUsers: Obtiene los usuarios de una empresa en la colección de usaurio \n
       @params: 
         company: Contiene el id mongo de la empresa
    '''
    print("In obtainUsers:", company)
    resp = user.getUsersByCompany(company)
    return jsonify(resp)
