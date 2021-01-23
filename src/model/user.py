'''
   user

   Administra los acceso de la DB a la colección de usuario donde se guardan los datos de los usuarios del sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Vitt Inversiones SAS - vitt.co
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src.mongoCRUD import connector
from config import MONGO, DB, SECRET_KEY
import bcrypt
### Nombre de la colección en la DB que se utilizará
coleccion = 'usuario'

# Métodos CRUD en la coleeción usuario
def adduserClient(usuario, empresa):
  '''
     addUser: Crea un usuario en la coleeción de usaurio \n
     @params: 
       usuario: objeto Json con los campos a insertar en la DB 
       empresa: Id de la empresa a la que se asocia el usuario a crear
  '''
  print("In addUser:", empresa)
  usuario['salario'] = int(usuario['salario'])
  usuario['empresa'] = empresa
  clave = str(usuario['clave']).encode()
  encripted = bcrypt.hashpw(clave, SECRET_KEY)
  usuario['clave'] = encripted
  try:
    verify = getUserByUsuario({'id_usuario': usuario['id_usuario']})
    if verify == None:
      user = connector.addToCollection(MONGO, DB, coleccion, usuario)
      return {'response': 'OK', 'message': 'Usuario creado ' + str(user)}
    else:
      return {'response': 'ERROR', 'message': 'Ya existe un usuario con el mismo id'}
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}

def getUserById(idMongo):
  '''
     getUserById: Busca un usuario en la coleeción de usaurio por el '_id' \n
     @params: 
       idMongo: Id del objeto usuario a buscar en la DB 
  '''
  print("In getUserById:", idMongo)
  try:
    resp = connector.getCollectionById(MONGO, DB, coleccion, idMongo)
    return {'response': 'OK', 'data': resp}
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + idMongo}

def getUserByUsuario(usuario):
  '''
     getUserByUsuario: Busca un usuario en la coleeción de usaurio por el 'id_usuario' \n
     @params: 
       usuario: Id del objeto usuario a buscar en la DB 
  '''
  print("In getUserByUsuario:", usuario)
  try:
    resp = connector.getCollecctionByField(MONGO, DB, coleccion, {"id_usuario" : usuario})
    return {'response': 'OK', 'data': resp}
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + usuario}

def getUsersByCompany(idCompany):
  '''
     getUsers: Busca todos los usuario de una empresa en la coleeción de usaurio \n
     @params: 
       idCompany: Id de la empresa a la que está asociado el usuario en la DB 
  '''
  print("In getUsersByCompany:", idCompany)
  try:
    result = connector.getCollecctionsByField(MONGO, DB, coleccion, {'empresa': idCompany})
    return {'response': 'OK', 'data': result}
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar los usuarios de la empresa: ' + idCompany}

def deleteUserById(idUsuario):
  '''
     deleteUserById: Elimina un usuario de la colección \n
     @params: 
       idUsuario: Id del objeto usuario a eliminar en la DB 
  '''
  print("In deleteUserById:", idUsuario)
  try:
    result = connector.deleteById(MONGO, DB, coleccion, idUsuario)
    return {'response': 'OK', 'message': 'User Deleted', 'data': result}
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al eliminar el usuario: ' + idUsuario}

def updateUserById(usuario):
  '''
     updateUserById: Actualiza un usuario en la colección de usaurio \n
     @params: 
       usuario: objeto usuario con todos los datos a modificar en la DB 
  '''
  print("In updateUserById:", usuario['_id'])
  try:
    result = connector.updateById(MONGO, DB, coleccion, usuario)
    return {'response': 'OK', 'message': 'User Updated', 'data': result}
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al modificar el usuario: ' + usuario['id_usuario']}

def updateUserPassword(usuario):
  '''
     updateUserPassword: Actualiza la contraseña de un usuario en la colección de usaurio \n
     @params: 
        usuario: objeto Json con los datos de usuario para modificar en la DB, sólo toma _'id', 'id_usuario', 'clave_actual' y 'nueva_clave' 
  '''
  print("In updateUserPassword:", usuario['_id'])
  try:
    verifica = validatePassword({'id_usuario': usuario['id_usuario'], 'clave': usuario['clave_actual']}
    if  verifica == 'OK':
      result = connector.updateById(MONGO, DB, coleccion, usuario)
      return {'response': 'OK', 'message': 'Password Updated', 'data': result}
    else:
      return {'response': 'ERROR', 'message': verifica}
  except:
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
  except:
    return {'response':'ERROR', 'message':'Se presentó un error validando el usuario'}
