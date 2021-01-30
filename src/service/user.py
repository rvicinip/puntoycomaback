'''
   user

   Realiza todas las transacciones y tareas necesarias para mantener los datos de los usuarios en el sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src.service import privated
from src import app
from src.model import user
from flask import jsonify, request

@app.route('/user', methods = ['POST'])
@privated
def createUser():
   '''
      createUser: Crea un usuario de la empresa en la coleeción de usaurio \n
   '''
   ## Validad que se enviarion todos los campos
   if not 'id_usuario' in request.json:
      return {'response':'ERROR', 'message': 'Cédula es obligatoria¿o, por favor verifíque'}
   if not 'nombre' in request.json:
      return {'response':'ERROR', 'message': 'Nombre del empleado es obligatorio, por favor verifíque'}
   if not 'empresa' in request.json:
      return {'response':'ERROR', 'message': 'Empresa es obligatorio, por favor verifíque'}
   if not 'clave' in request.json:
      return {'response':'ERROR', 'message': 'Contraseña es obligatorio, por favor verifíque'}
   dato = request.json
   print("In createUser:", dato['id_usuario'])
   if not dato['id_usuario']:
      return {'response':'ERROR', 'message': 'Cédula es obligatorio, por favor verifíque'}
   if not dato['nombre']:
      return {'response':'ERROR', 'message': 'Nombre del empleado es obligatorio, por favor verifíque'}
   if not dato['empresa']:
      return {'response':'ERROR', 'message': 'Empresa es obligatorio, por favor verifíque'}
   if not dato['clave']:
      return {'response':'ERROR', 'message': 'Contraseña es obligatorio, por favor verifíque'}
   ## Guarda un nuevo usuario en la DB
   dato = request.json
   resp = user.addUserEmpresa(dato)
   return jsonify(resp)

@app.route('/user/clave', methods = ['POST'])
@privated
def changePassword(usuario):
   '''
      changePassword: Actualiza la contraseña de un usuario \n
   '''
   print("In changePassword")
   ## Validad que se enviarion todos los campos
   if not 'id_usuario' in request.json:
      return {'response':'ERROR', 'message': 'Cédula es obligatoria¿o, por favor verifíque'}
   if not 'clave' in request.json:
      return {'response':'ERROR', 'message': 'Contraseña es obligatorio, por favor verifíque'}
   if not 'nueva_clave' in request.json:
      return {'response':'ERROR', 'message': 'Nueva contraseña es obligatorio, por favor verifíque'}
   dato = request.json
   print("In createUser:", dato['id_usuario'])
   if usuario['id_usuario'] != dato['id_usuario']:
      return {'response':'ERROR', 'message': 'Usuario autenticado no corresponde, por favor verifíque'}
   if not dato['id_usuario']:
      return {'response':'ERROR', 'message': 'Cédula es obligatorio, por favor verifíque'}
   if not dato['clave']:
      return {'response':'ERROR', 'message': 'Contraseña es obligatorio, por favor verifíque'}
   if not dato['nueva_clave']:
      return {'response':'ERROR', 'message': 'Nueva contraseña es obligatorio, por favor verifíque'}
   ## Guarda una nueva empresa en la DB
   resp = user.updateUserPassword(dato)
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
