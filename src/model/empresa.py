'''
   empresa

   Administra los acceso de la DB a la colección de empresa donde se guardan los datos de las empresas del sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia - venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from bson import ObjectId
from operator import itemgetter
from src.mongoCRUD import connector
from src.utility import xlsReader
from src.model import user
from config import MONGO, DB
import traceback

### Constantes de la colecciones
DICCOLL = 'diccionario'
EMPCOLL = 'empresa'
FRECOLL = 'frecuencia'

# Métodos CRUD en la coleeción usuario
def addCompany(empresa):
  '''
     addCompany: Crea un usuario en la coleeción de usaurio \n
     @params: 
       empresa: objeto Json con los campos a insertar en la DB 
  '''
  print("In addCompany:", empresa['nit'])
  try:
    verifica = getCompanyByNIT(empresa['nit'])
    if 'data' in verifica:
      return {'response': 'ERROR', 'message': 'Ya existe una empresa con el mismo NIT'}    
    resp = connector.addToCollection(MONGO, DB, EMPCOLL, empresa)
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
    resp = connector.getCollectionById(MONGO, DB, EMPCOLL, idMongo)
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
    resp = connector.getCollecctionByField(MONGO, DB, EMPCOLL, {"nit" : nit})
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR']}
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar la empresa: ' + nit}

def addDiccionario(diccionario, company, niveles):
  '''
     addDiccionario: Crea los registro de un diccionario, asociaciados a una empresa \n
     @params: 
       diccionario: objeto con los datos de los proceso de la compañia
       company: id de la empresa a la que pertenece el diccionario
       niveles: Cantidad de niveles que tiene el documento que se está guardando
  '''
  print("In addDiccionario:", company)
  try:
    lector = xlsReader.readXLS(diccionario, 1)
    if 'ERROR' in lector:
      return {'response': 'ERROR', 'message': lector['ERROR']}
    valida = xlsReader.validateXLS(lector, ['nombre', 'nivel'])
    if 'ERROR' in valida:
      return {'response': 'ERROR', 'message': valida['ERROR'], 'data': valida['data']}
    lector = sorted(lector, key=itemgetter('nivel'))
    lista = []
    err   = []
    for dic in lector:
      dic['empresa'] = company
      padre = str(dic['padre'])
      if ',' in padre:
        padre.replace(',', '.')
        dic['padre'] = padre
      actividad = str(dic['id_actividad'])
      if ',' in actividad:
        actividad.replace(',', '.')
        dic['id_actividad'] = actividad
      revisa = getActivity(dic['empresa'], dic['id_actividad'])
      if revisa['response'] == 'ERROR':
        if int(dic['nivel']) > 1:
          papa = getActivity(dic['empresa'], dic['padre'])
          if papa['response'] == 'ERROR':
            err.append({'response': papa['message'] + ' en la validación del padre', 'data': dic})
            dic = {}
          else:
            papa = papa['data']
            dic['id_padre'] = papa['_id']
        resp = connector.addToCollection(MONGO, DB, DICCOLL, dic)
        if not ObjectId.is_valid(resp):
          err.append({'response': resp['ERROR'], 'data': dic})
        else:
          dic['_id'] = resp
          lista.append(resp)
      else:
        err.append({'response': 'Ya existe una actividad con ese id en la empresa', 'data': dic})
    return {'response': 'OK','data': lista, 'error': err}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error procesando el diccionario ' + diccionario.filename}
  
def getActivity(company, activity):
  '''
     getActivity: Crea los registro de un diccionario, asociaciados a una empresa \n
     @params: 
       company: id de la empresa a la que pertenece la actividad
       activity: Código de la actividad 'id_actividad'
  '''
  print("In getActivity:", activity, company)
  try:
    resp = connector.getCollecctionByField(MONGO, DB, DICCOLL, {'empresa': company, 'id_actividad': activity})
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR']}
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un consultando la actividad ' + activity}

def addFrecuacia(frecuencia, company):
  '''
     addFrecuacia: Crea los registro de un diccionario, asociaciados a una empresa \n
     @params: 
       frecuencia: objeto con los datos de los tiempos y frecuencias de la compañia
       company: id de la empresa a la que pertenecen las frecuencias
  '''
  print("In addFrecuacia:", company)
  try:
    lector = xlsReader.readXLS(frecuencia, 1)
    if 'ERROR' in lector:
      return {'response': 'ERROR', 'message': lector['ERROR']}
    valida = xlsReader.validateXLS(lector, ['nombre',	'tipo',	'valor'])
    if 'ERROR' in valida:
      return {'response': 'ERROR', 'message': valida['ERROR'], 'data': valida['data']}
    lista = []
    err   = []
    for dic in lector:
      dic['empresa'] = company
      valor = float(dic['valor'])
      if valor <= 0 :
        err.append({'response': 'el valor de la frecuencia debe ser mayor a 0', 'data': dic})
        dic = {}
      tipo = int(dic['tipo'])
      if tipo == 1:
         dic['tipo']= {'tipo': tipo, 'nombre': 'Tiempo'}
      elif tipo == 2:
         dic['tipo']= {'tipo': tipo, 'nombre': 'Frecuencia'}
      revisa = getFrecuencia(dic['empresa'], dic['nombre'])
      if revisa['response'] == 'ERROR':
        resp = connector.addToCollection(MONGO, DB, FRECOLL, dic)
        if not ObjectId.is_valid(resp):
          err.append({'response': resp['ERROR'], 'data': dic})
        else:
          dic['_id'] = resp
          lista.append(resp)
      else:
        err.append({'response': 'Ya existe esta frecuencia en la empresa', 'data': dic})
    return {'message': 'OK', 'data': lista, 'error': err}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error procesando la frecuencia ' + frecuencia.filename}

def getFrecuencia(company, frecuency):
  '''
     getFrecuencia: Crea los registro de un diccionario, asociaciados a una empresa \n
     @params: 
       company: id de la empresa a la que pertenece la actividad
       frecuency: Nombre de la frecuencia 'nombre'
  '''
  print("In getFrecuencia:", frecuency, company)
  try:
    resp = connector.getCollecctionByField(MONGO, DB, FRECOLL, {'empresa': company, 'nombre': frecuency})
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR']}
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un consultando la actividad ' + frecuency}

def addEmpleado(usuario, company):
  '''
     addEmpleados: Crea los registro de los empleados asociaciados a una empresa \n
     @params: 
       usuario: objeto con los datos de los empleados de la compañia
       company: id de la empresa a la que pertenecen los usuarios
  '''
  print("In addEmpleados:", company)
  try:
    lector = xlsReader.readXLS(usuario, 1)
    if 'ERROR' in lector:
      return {'response': 'ERROR', 'message': lector['ERROR']}
    campos = ['id_usuario',	'clave',	'nombre',	'salario',	'jornada',	'email',	'cargo',	'centrocosto',	'tipocontrato']
    valida = xlsReader.validateXLS(lector, campos)
    if 'ERROR' in valida:
      return {'response': 'ERROR', 'message': valida['ERROR'], 'data': valida['data']}
    lista = []
    err   = []
    for dic in lector:
      resp = user.adduserClient(dic, company)
      if not ObjectId.is_valid(resp):
        err.append({'response': resp['ERROR'], 'data': dic})
      else:
        dic['_id'] = resp
        lista.append(resp)
    return {'response': 'OK','data': lista, 'error': err}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error procesando los empleados ' + usuario.filename}