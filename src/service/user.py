'''
   user:
      Administra los servicios para mantener los datos de los usuarios en el sistema

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
def createUser(usuario):
   '''
      createUser: Crea un usuario de la empresa en la coleeción de usaurio \n
   '''
   ## Validad que se enviarion todos los campos
   dato = request.json
   print("In createUser:", dato)
   campos = ['id_usuario', 'nombre', 'empresa', 'clave']
   valida = validateFields(campos, dato)
   if valida['response'] == 'ERROR':
      return jsonify(valida)
   resp = user.addUserEmpresa(dato)
   return jsonify(resp)

@app.route('/users/<company>', methods = ['GET'])
@privated
def obtainUsers(usuario, company):
    '''
       obtainUsers: Obtiene los usuarios de una empresa en la colección de usaurio \n
       @params: 
         company: Contiene el id mongo de la empresa
    '''
    print("In obtainUsers:", company)
    resp = user.getUsersByCompany(company)
    return jsonify(resp)

@app.route('/users/status/<company>', methods = ['GET'])
@privated
def statusIndices(usuario, company):
    '''
       statusIndices: Obtiene los indices de cada estado de los empleados de una empresa \n
       @params: 
         company: Nit de la empresa
    '''
    print("In statusIndices:", company)
    resp = user.statusList(company)
    return jsonify(resp)

@app.route('/users/close-inquest', methods = ['PUT'])
@privated
def closeUserInquest(usuario):
    '''
       closeUserInquest: Cierra la encuesta que está realizando el usuario
    '''
    print("In closeUserInquest")
    resp = user.closeInquest(usuario['id_usuaruio'])
    return jsonify(resp)
