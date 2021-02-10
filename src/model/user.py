'''
   user

   Administra los acceso de la DB a la colección de usuario donde se guardan los datos de los usuarios del sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Vitt Inversiones SAS - vitt.co
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from bson import ObjectId
from random import randint
from src.utility import mailer
from src.mongoCRUD import connector
from config import MONGO, DB
import bcrypt
import traceback
### Nombre de la colección en la DB que se utilizará
USUCOLL = 'usuario'

# Métodos CRUD en la coleeción usuario
### CREA
def addUserClient(usuario, empresa):
  '''
     addUser: Crea un usuario en la colección de usaurio \n
     @params: 
       usuario: objeto Json con los campos a insertar en la DB 
       empresa: Id mongo de la empresa a la que se asocia el usuario a crear
  '''
  print("In addUserClient:", empresa)
  usuario['salario'] = int(usuario['salario'])
  usuario['empresa'] = empresa
  usuario['perfil'] = 'client'
  usuario['estado'] = 'A' ## A indica que el estado del usuario es activo
  clave = str(usuario['clave']).encode()
  encripted = bcrypt.hashpw(clave, bcrypt.gensalt(12))
  usuario['clave'] = encripted.decode('utf-8')
  try:
    verifica = getUserByUsuario(usuario['id_usuario'])
    if not 'data' in verifica:
      resp = connector.addToCollection(MONGO, DB, USUCOLL, usuario)
      if not ObjectId.is_valid(str(resp)):
        return {'response': 'ERROR', 'message': resp['ERROR']}
      usuario['_id'] = str(ObjectId(resp))
      usuario.pop('clave')
      return {'response': 'OK', 'message': 'Usuario creado ', 'data': usuario}
    return {'response': 'ERROR', 'message': 'Ya existe un usuario con el mismo id'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}

def addUserEmpresa(usuario):
  '''
     addUserEmpresa: Crea un usuario consultor en la colección de usaurio \n
     @params: 
       usuario: objeto Json con los campos a insertar en la DB 
       empresa: Id mongo de la empresa a la que se asocia el usuario a crear
  '''
  print("In addUserEmpresa")
  if 'salario' in usuario:
    usuario['salario'] = int(usuario['salario'])
  usuario['perfil'] = 'consult'
  usuario['estado'] = 'A' ## A indica que el estado del usuario es activo
  clave = str(usuario['clave']).encode()
  encripted = bcrypt.hashpw(clave, bcrypt.gensalt(12))
  usuario['clave'] = encripted.decode('utf-8')
  try:
    verifica = getUserByUsuario(usuario['id_usuario'])
    if not 'data' in verifica:
      resp = connector.addToCollection(MONGO, DB, USUCOLL, usuario)
      if not ObjectId.is_valid(str(resp)):
        return {'response': 'ERROR', 'message': resp['ERROR']}
      usuario['_id'] = str(ObjectId(resp))
      usuario.pop('clave')
      return {'response': 'OK', 'message': 'Usuario creado ', 'data': usuario}
    return {'response': 'ERROR', 'message': 'Ya existe el usuario', 'data': verifica}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}

### LEE
def getUserById(idMongo):
  '''
     getUserById: Busca un usuario en la coleeción de usaurio por el '_id' \n
     @params: 
       idMongo: Id del objeto usuario a buscar en la DB 
  '''
  print("In getUserById:", idMongo)
  try:
    resp = connector.getCollectionById(MONGO, DB, USUCOLL, idMongo)
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR']}
    resp.pop('clave')
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + idMongo}

def getUserByUsuario(usuario):
  '''
     getUserByUsuario: Busca un usuario en la coleeción de usaurio por el 'id_usuario' \n
     @params: 
       usuario: Id del objeto usuario a buscar en la DB 
  '''
  print("In getUserByUsuario:", usuario)
  try:
    resp = connector.getCollecctionByField(MONGO, DB, USUCOLL, {"id_usuario" : usuario})
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR']}
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + usuario}

def getUsersByCompany(idCompany):
  '''
     getUsersByCompany: Busca todos los usuario de una empresa en la coleeción de usaurio \n
     @params: 
       idCompany: Id mongo de la empresa a la que está asociado el usuario en la DB 
  '''
  print("In getUsersByCompany:", idCompany)
  try:
    resp = connector.getCollecctionsByField(MONGO, DB, USUCOLL, {'empresa': idCompany})
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR'] + ' in getUsersByCompany'}
    for r in resp:
      r.pop('clave')
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar los usuarios de la empresa: ' + idCompany}

def recallUserPassword(idUsuario):
  '''
     recallUserPassword: genera y envía un código para recuperar la contraseña de una cuenta \n
     @params: 
        idUsuario: nombre de usuario 'id_usuario' del cliente a recuperar contraseña
  '''
  print("In recallUserPassword:", idUsuario)
  resp = getUserByUsuario(idUsuario)
  if resp['response'] == 'ERROR':
    return resp
  urc = resp['data']
  if urc['email'] == '':
    return {'response': 'NOMAIL', 'data': urc}
  codigo = randint(100000, 999999)
  mensaje = 'Para el cambio de la clave de seguiridad tu cuenta, por favor confirme con el siguente codigo ' + str(codigo)
  urc['codigo'] = int(codigo)
  urc.pop('clave')
  upd = updateUserById(urc)
  if upd['response'] == 'OK':
    valida = upd['data']  
    mail = mailer.sendMail(valida['email'], mensaje)
    if mail['response'] == 'OK':
      return {'response': 'OK', 'message': 'correo enviado a ' + valida['email']}
    return mail
  return upd

def validateCodigo(usuario):
  '''
     validateCodigo: Valida que código corresponda con el enviado al usuario y habilita el cambio de contraseña \n
     @params: 
        usuario: objeto Json con los datos de usuario para validar 'id_usuario', 'nueva_clave' y 'codigo' 
  '''
  print("In validateCodigo:", usuario['id_usuario'])
  try:
    datos = getUserByUsuario(usuario['id_usuario'])
    if datos['response'] == 'OK':
      values = datos['data']
      print('values', values['codigo'], 'usuario', usuario['codigo'])
      if int(values['codigo']) == int(usuario['codigo']):
        usuario['_id'] = values['_id']
        return updatePasswordByCodigo(usuario)
      return {'response':'ERROR', 'message':'El código no concuerda'}
    return datos
  except Exception:
    traceback.print_exc()
    return {'response':'ERROR', 'message':'Se presentó un error validando el código del usuario'}

def validatePassword(usuario):
  '''
     validatePassword: Valida que la contraseña corresponda con el usuario en la DB \n
     @params: 
        usuario: objeto Json con los datos de usuario para validar en la DB, sólo toma 'id_usuario' y 'clave' 
  '''
  print("In validatePassword:", usuario['id_usuario'])
  try:
    verifica = getUserByUsuario(usuario['id_usuario'])
    if verifica['response'] == 'OK':
      resp = verifica['data']
      if bcrypt.checkpw(str(usuario['clave']).encode(), str(resp['clave']).encode()):
        return {'response':'OK', 'data': resp}
      return {'response':'ERROR', 'message':'Contraseña errada'}
    return verifica
  except Exception:
    traceback.print_exc()
    return {'response':'ERROR', 'message':'Se presentó un error validando el usuario'}

### ACTUALIZA
def updateUserById(usuario):
  '''
     updateUserById: Actualiza un usuario en la colección de usaurio \n
     @params:
       usuario: objeto usuario con todos los datos a modificar en la DB 
  '''
  print("In updateUserById:", usuario['_id'])
  try:
    if 'clave' in usuario:
      usuario.pop('clave')
    resp = connector.updateById(MONGO, DB, USUCOLL, usuario)
    if not resp.acknowledged:
        return {'response': 'ERROR', 'message': 'No se actualizó el usuario'}
    return {'response': 'OK', 'message': 'Usuario actualizado', 'data': usuario}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al modificar el usuario: ' + usuario['id_usuario']}

def updateUserPassword(usuario):
  '''
     updateUserPassword: Actualiza la contraseña de un usuario en la colección de usaurio \n
     @params: 
        usuario: objeto Json con los datos de usuario para modificar en la DB, sólo toma _'id', 'id_usuario', 'clave' y 'nueva_clave' 
  '''
  print("In updateUserPassword:", usuario['id_usuario'])
  try:
    verifica = validatePassword({'id_usuario': usuario['id_usuario'], 'clave': usuario['clave']})
    if  verifica['response'] == 'OK':
      nuevaClave = str(usuario['nueva_clave']).encode()
      encripted = bcrypt.hashpw(nuevaClave, bcrypt.gensalt(12))
      usuario['clave'] = encripted.decode('utf-8')
      usuario.pop('nueva_clave')
      resp = connector.updateById(MONGO, DB, USUCOLL, usuario)
      if not resp.acknowledged:
        return {'response': 'ERROR', 'message': 'No se actualizó la contraseña'}
      return {'response': 'OK', 'message': 'Contraseña actualizada'}
    return verifica
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al modificar el usuario: ' + usuario['id_usuario']}

def updatePasswordByCodigo(usuario):
  '''
     updatePasswordByCodigo: Actualiza la contraseña de un usuario despues de validar el código \n
     @params: 
        usuario: Objeto Json con los datos ('id_usuario', 'nueva_clave') del usuario para habilitar modificar la contraseña
  '''
  print("In updatePasswordByCodigo")
  try:
    nuevaClave = str(usuario['nueva_clave']).encode()
    encripted = bcrypt.hashpw(nuevaClave, bcrypt.gensalt(12))
    usuario['clave'] = encripted.decode('utf-8')
    usuario.pop('nueva_clave')
    usuario['codigo'] = 0
    resp = connector.updateById(MONGO, DB, USUCOLL, usuario)
    if not resp.acknowledged:
      return {'response': 'ERROR', 'message': 'No se actualizó la contraseña'}
    return {'response': 'OK', 'message': 'Contraseña actualizada'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al modificar el usuario: ' + usuario['id_usuario']}

### ELIMINA
def deleteUserById(idUsuario):
  '''
     deleteUserById: Elimina un usuario de la colección \n
     @params: 
       idUsuario: Id del objeto usuario a eliminar en la DB 
  '''
  print("In deleteUserById:", idUsuario)
  try:
    resp = connector.deleteById(MONGO, DB, USUCOLL, idUsuario)
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR']}
    return {'response': 'OK', 'message': 'Usuario borrado'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al eliminar el usuario: ' + idUsuario}
