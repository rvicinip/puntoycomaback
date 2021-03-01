'''
   empresa

   Administra los acceso de la DB a la colección de empresa donde se guardan los datos de las empresas del sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia - venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src.mysqlConnector.empresa import Empresa
from src.model import user, frecuencia, diccionario
from src import db
import traceback

# Métodos CRUD en las coleeciones diccionario, empresa y frecuencias
### CREA
def addCompany(emp):
  '''
     addCompany: Crea una empresa en la DB \n
     @params: 
       empresa: objeto Json con los campos a insertar en la DB 
  '''
  print("In addCompany:", emp['nit'])
  try:
    verifica = getCompanyByNIT(emp['nit'])
    if 'data' in verifica:
      return {'response': 'ERROR', 'message': 'Ya existe una empresa con el mismo NIT'}    
    emp['tipo'] = 'client'
    emp['estado'] = 'A'
    comp = Empresa(emp)
    db.session.add(comp)
    db.session.commit()
    return {'response': 'OK', 'message': 'Empresa creada ', 'data': emp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}

### LEE
def getAllCompanies():
  '''
     getAllCompanies: Busca todas las empresas en DB \n
  '''
  print("In getAllCompanies")
  try:
    resp = []
    emps = Empresa.query.all()
    for e in emps:
      resp.append(e.toJSON())
    if len(resp) > 0:
      return {'response': 'OK', 'data': resp}
    return {'response': 'ERROR', 'message': 'No se encontraron empresas'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar las empresas'}

def getCompanyByNIT(idEmp):
  '''
     getCompanyByNIT: Busca una empresa en la coleeción de empresas por el 'nit' \n
     @params:
       idEmp: Id del objeto usuario a buscar en la DB 
  '''
  print("In getCompanyByNIT:", idEmp)
  try:
    resp = Empresa.query.filter(Empresa.nit == idEmp, Empresa.estado == 'A').first()
    if resp:
      return {'response': 'OK', 'data': resp.toJSON()}
    return {'response': 'ERROR', 'message': 'No se encontró la empresa ' + str(idEmp)}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + str(idEmp)}

def getFullCompanyByNIT(idEmp):
  '''
     getFullCompanyById: Busca una empresa acorde a su 'nit' y devuelve toda su información, diccionario, empleados y frecuencias \n
     @params: 
       idEmp: NIT de la empresa a buscar en la DB 
  '''
  print("In getFullCompanyByNIT:", idEmp)
  try:
    company = getCompanyByNIT(idEmp)
    dicc = diccionario.getDiccionarioByCompany(idEmp)
    if dicc['response'] == 'ERROR':
      return dicc
    frec = frecuencia.getFrecuenciasByCompany(idEmp)
    if frec['response'] == 'ERROR':
      return frec
    empleado = user.getUsersByCompany(idEmp)
    if empleado['response'] == 'ERROR':
      return empleado
    resp = {'empresa': company['data'], 'diccionario': dicc['data'], 'frecuencia': frec['data'], 'empleado': empleado['data']}
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar la empresa: ' + idEmp}

def getDictsFrecs(idEmp):
  '''
     getDictsFrecs: Busca el diccionario y las frecuencias de una empresa acorde a su 'nit' \n
     @params: 
       idMongo: id Mongo de la empresa a buscar en la DB 
  '''
  print("In getDictsFrecs:", idEmp)
  try:
    dicc = diccionario.getDiccionarioByCompany(idEmp)
    if dicc['response'] == 'ERROR':
      return dicc
    frec = frecuencia.getFrecuenciasByCompany(idEmp)
    if frec['response'] == 'ERROR':
      return frec
    return {'response': 'OK', 'frecuencia': frec['data'], 'diccionario': dicc['data']}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar la empresa: ' + idEmp}

### ACTUALIZA
def updateCompany(emp):
  '''
     updateCompany: Modifica una empresa en la DB \n
     @params: 
       empresa: objeto Json con los campos a actualizar en la DB 
  '''
  print("In updateCompany:", emp['nit'])
  try:
    verifica = getCompanyByNIT(emp['nit'])
    if verifica['response'] == 'OK':
      value = verifica['data']
      if value['nit'] != emp['nit']:
        return {'response': 'ERROR', 'message': 'No se puede modificar el NIT'}
      resp = Empresa.query.filter(Empresa.nit == emp['nit']).update({
                                  Empresa.nombre  : emp['nombre'],
                                  Empresa.niveles : emp['niveles'],
                                  Empresa.estado  : emp['estado']
      })
      db.session.commit()
      return {'response': 'OK', 'message': str(resp) + ' Empresa actualizada'}
    return {'response': 'ERROR', 'message': 'No se existe la empresa' + emp['nit']}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}

def deleteCompany(idEmp):
  '''
     deleteCompany: Modifica el estado a "D" en una empresa en la DB \n
     @params: 
       idEmp: Nit de la empresa a eliminar en la DB 
  '''
  print("In deleteCompany:", idEmp)
  try:
    verifica = getCompanyByNIT(idEmp)
    if verifica['response'] == 'OK':
      value = verifica['data']
      if value['nit'] != idEmp:
        return {'response': 'ERROR', 'message': 'No se puede modificar el NIT'}
      resp = Empresa.query.filter(Empresa.nit == idEmp).update({
                                  Empresa.estado  : "D"  ## Indica que la empresa se encuentra inactiva
      })
      db.session.commit()
      return {'response': 'OK', 'message': str(resp) + ' Empresa eliminada'}
    return verifica
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}