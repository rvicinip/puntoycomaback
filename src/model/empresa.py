'''
   empresa

   Administra los acceso de la DB a la colección de empresa donde se guardan los datos de las empresas del sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia - venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from bson import ObjectId
from src.mongoCRUD import connector
from config import MONGO, DB
import traceback

# Métodos CRUD en la coleeción usuario
def addCompany(empresa):
  '''
     addCompany: Crea un usuario en la coleeción de usaurio \n
     @params: 
       empresa: objeto Json con los campos a insertar en la DB 
  '''
  print("In addCompany:", empresa['nombre'])
  try:
    verifica = getCompanyByNIT(empresa['nit'])
    if 'data' in verifica:
      return {'response': 'ERROR', 'message': 'Ya existe una empresa con el mismo NIT'}
    
    resp = connector.addToCollection(MONGO, DB, 'empresa', empresa)
    if not ObjectId.is_valid(resp):
      return {'response': 'ERROR', 'message': resp['ERROR']}
    
    empresa['_id'] = str(ObjectId(resp))
    return {'response': 'OK', 'message': 'Usuario creado ', 'data': empresa}

  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}


def getCompanyById(idMongo):
  '''
     getCompanyById: Busca una empresa en la coleeción de empresas por el '_id' \n
     @params:
       idMongo: Id del objeto usuario a buscar en la DB 
  '''
  print("In getCompanyById:", idMongo)
  try:
    resp = connector.getCollectionById(MONGO, DB, 'empresa', idMongo)
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR']}

    return {'response': 'OK', 'data': resp}

  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + idMongo}

def getCompanyByNIT(nit):
  '''
     getCompanyByNIT: Busca una empresa en la coleeción de empresas por el 'nit' \n
     @params: 
       nit: Nit de la empresa a buscar en la DB 
  '''
  print("In getCompanyByNIT:", nit)
  try:
    resp = connector.getCollecctionByField(MONGO, DB, 'empresa', {"nit" : nit})
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR']}

    return {'response': 'OK', 'data': resp}

  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar la empresa: ' + nit}
