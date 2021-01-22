'''
   user

   Administra los acceso de la DB a la colección de usuario donde se guardan los datos de los usuarios del sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src.mongoCRUD import connector
from config import MONGO, DB
import json

### Nombre de la colección en la DB que se utilizará
coleccion = 'usuario'

# Métodos CRUD en la coleeción usuario
def addUser(usuario, empresa):
  '''
     :addUser: Crea un usuario en la coleeción de usaurio
     :params: 
       usuario: objeto Json con los campos a insertar en la DB 
       empresa: Id de la empresa a la que se asocia el usuario a crear
  '''
  print("In addUser:", empresa)
  usuario['salario'] = int(usuario['salario'])
  usuario['empresa'] = empresa
  try:
    user = connector.addToCollection(MONGO, DB, coleccion, usuario)
    return {'response': 'OK', 'message': 'Usuario creado ' + str(ObjectId(user))}
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}

def getUserById(idMongo):
  '''
     :getUserById: Busca un usuario en la coleeción de usaurio por el _id
     :params: idMongo: Id del objeto usuario a buscar en la DB 
  '''
  print("In getUserById:", idMongo)
  try:
    resp = connector.getCollectionById(MONGO, DB, coleccion, idMongo)
    return resp
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + idMongo}

def getUserByUsuario(usuario):
  '''
     :getUserByUsuario: Busca un usuario en la coleeción de usaurio por el id_usuario
     :params: usuario: Id del objeto usuario a buscar en la DB 
  '''
  print("In getUserByUsuario:", usuario)
  try:
    resp = connector.getCollecctionByField(MONGO, DB, coleccion, {"id_usuario" : usuario})
    return resp
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + usuario}

def getUsersByCompany(idCompany):
  '''
     :getUsers: Busca todos los usuario de una empresa en la coleeción de usaurio
     :params: idCompany: Id de la empresa a la que está asociado el usuario en la DB 
  '''
  print("In getUsersByCompany:", idCompany)
  try:
    result = connector.getCollecctionsByField(MONGO, DB, coleccion, {'empresa': idCompany})
    return result
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar los usuarios de la empresa: ' + idCompany}

def deleteUserById(idUsuario):
  '''
     :deleteUserById: Elimina un usuario de la colección
     :params: idUsuario: Id del objeto usuario a eliminar en la DB 
  '''
  print("In deleteUserById:", idUsuario)
  try:
    result = connector.deleteById(MONGO, DB, coleccion, idUsuario)
    return {'response': 'OK', 'message': 'User Deleted', 'data': result}
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al eliminar el usuario: ' + idUsuario}

def updateUserById(usuario):
  '''
     :updateUserById: Actualiza un usuario en la colección de usaurio
     :params: idUsuario: Id del objeto usuario a buscar en la DB 
  '''
  print("In updateUserById:", usuario)
  try:
    result = connector.updateById(MONGO, DB, coleccion, usuario)
    return {'response': 'ERROR', 'message': 'User Updated', 'data': result}
  except:
    return {'response': 'ERROR', 'message': 'Se presentó un error al modificar el usuario: ' + usuario['id_usuario']}
