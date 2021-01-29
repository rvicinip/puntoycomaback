'''
   user

   Administra los acceso de la DB a la colección de usuario donde se guardan los datos de los usuarios del sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Vitt Inversiones SAS - vitt.co
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from bson import ObjectId
from src.mongoCRUD import connector
from config import MONGO, DB
import bcrypt
import traceback
### Nombre de la colección en la DB que se utilizará
USUCOLL = 'usuario'

# Métodos CRUD en la coleeción usuario
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
  usuario['clave'] = encripted
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
    print(__name__)
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
  usuario['clave'] = encripted
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
    print(__name__)
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}

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
    print(__name__)
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
    resp.pop('clave')
    return {'response': 'OK', 'data': resp}
  except Exception:
    print(__name__)
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
      return {'response': 'ERROR', 'message': resp['ERROR']}
    for r in resp:
      r.pop('clave')
    return {'response': 'OK', 'data': resp}
  except Exception:
    print(__name__)
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar los usuarios de la empresa: ' + idCompany}

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
    print(__name__)
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al eliminar el usuario: ' + idUsuario}

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
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR']}
    resp.pop('clave')
    return {'response': 'OK', 'message': 'User Updated', 'data': resp}
  except Exception:
    print(__name__)
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al modificar el usuario: ' + usuario['id_usuario']}

def updateUserPassword(usuario):
  '''
     updateUserPassword: Actualiza la contraseña de un usuario en la colección de usaurio \n
     @params: 
        usuario: objeto Json con los datos de usuario para modificar en la DB, sólo toma _'id', 'id_usuario', 'clave_actual' y 'nueva_clave' 
  '''
  print("In updateUserPassword:", usuario['_id'])
  try:
    verifica = validatePassword({'id_usuario': usuario['id_usuario'], 'clave': usuario['clave_actual']})
    if  verifica['response'] == 'OK':
      nuevaClave = str(usuario['nueva_clave']).encode()
      encripted = bcrypt.hashpw(nuevaClave, bcrypt.gensalt(12))
      usuario['clave'] = encripted
      resp = connector.updateById(MONGO, DB, USUCOLL, usuario)
      if 'ERROR' in resp:
        return {'response': 'ERROR', 'message': resp['ERROR']}
      return {'response': 'OK', 'message': 'Password Updated', 'data': resp}
    return verifica
  except Exception:
    print(__name__)
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al modificar el usuario: ' + usuario['id_usuario']}

### Este método no responde con objetos Json, para poder evaluar la respuesta directamente
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
      if bcrypt.checkpw(str(usuario['clave']).encode, verifica['clave']):
        return {'response':'OK', 'data': verifica}
      else:
        return {'response':'ERROR', 'message':'Contraseña errada'}
    else:
      return {'response':'ERROR', 'message':'No existe el usuario'}
  except Exception:
    print(__name__)
    traceback.print_exc()
    return {'response':'ERROR', 'message':'Se presentó un error validando el usuario'}