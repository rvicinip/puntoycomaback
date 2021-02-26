'''
   login

   Realiza las verificaciones y tareas necesarias para garantizar el acceso sólo a los usuarios registrados en el sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from flask import jsonify, request
import jwt
import datetime
from src import app
from src.model import user
from src.utility.validator import validateFields
from .protector import privated

@app.route('/')
def inicio():
   '''
      inicio: Busca todos los usuario de una empresa en la coleeción de usaurio \n
   '''
   print("In inicio \n")
    ## resp = usuario.getUsersByCompany('1asdc23')
   return jsonify({"inicio": "Servidor de backend de BPM Vena"})

@app.route('/access', methods = ['POST'])
def login():
   '''
      login: realiza las validaciones de usuario para permitir o no el ingreso a la aplicacion
   '''
   print("In login")
   data = request.json
   campos = ['id_usuario', 'clave']
   valida = validateFields(campos, data)
   if valida['response'] == 'OK':
      ingreso = user.validatePassword(data)
      if ingreso['response'] == 'ERROR':
        return jsonify(ingreso)
      usuario = ingreso['data']
      token = jwt.encode({'user' : usuario['id_usuario'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=5)}, app.config['SECRET_KEY'])
      return jsonify({'response': 'OK', 'data': usuario, 'token': token.decode('utf-8')})
   return jsonify(valida)

@app.route('/exit', methods = ['POST', 'GET'])
@privated
def logout(usuario):
    '''
       logout: Cierra la sesión de un usuario \n
    '''
    print("In logout", usuario)
    return jsonify({'response': 'OK', 'message': 'Sesión terminada'})

@app.route('/user/clave', methods = ['POST'])
@privated
def changePassword(usuario):
   '''
      changePassword: Actualiza la contraseña de un usuario \n
   '''
   print("In changePassword")
   ## Validad que se enviarion todos los campos
   dato = request.json
   campos = ['id_usuario', 'clave', 'nueva_clave']
   valida = validateFields(campos, dato)
   if valida['response'] == 'ERROR':
      return jsonify(valida)
   if dato['nueva_clave'] == dato['clave']:
      return jsonify({'response':'ERROR', 'message': 'La contraseña nueva debe ser diferente de la actual'})
   if usuario['id_usuario'] != dato['id_usuario']:
      return jsonify({'response':'ERROR', 'message': 'Usuario autenticado no corresponde, por favor verifíque'})
   dato['_id'] = usuario['_id']
   ## Actualiza la clave del usuario
   resp = user.updateUserPassword(dato)
   return jsonify(resp)

@app.route('/user/forget/<idUsuario>', methods = ['POST'])
def forgetPassword(idUsuario):
   '''
      forgetPassword: Genera un código para habilitar la actualización de la contraseña de un usuario \n
      @params: 
         idUsuario: id del usuario que utiliza para ingresar al sistema
   '''
   print("In forgetPassword", idUsuario)
   ## Validad que se enviarion todos los campos
   if not idUsuario:
      return jsonify({'response':'ERROR', 'message': 'Cédula es obligatorio, por favor verifíque'})
   resp = user.recallUserPassword(idUsuario)
   if resp['response'] == 'NOMAIL':
      return jsonify({'response': 'ERROR', 'message': 'El usuario ' + resp['data']['id_usuario'] + ' no tiene correo electrónico para recuperar la contraseña'})
   return jsonify(resp)

@app.route('/user/restore', methods = ['POST'])
def restorePassword():
   '''
      restorePassword: Valida el código y habilita la actualización de la contraseña de un usuario \n
   '''
   print("In restorePassword")
   ## Validad que se enviarion todos los campos
   dato = request.json
   campos = ['id_usuario', 'nueva_clave', 'codigo']
   valida = validateFields(campos, dato)
   if valida['response'] == 'ERROR':
      return jsonify(valida)
   print("valida", valida)
   resp = user.validateCodigo(dato)
   return jsonify(resp)
