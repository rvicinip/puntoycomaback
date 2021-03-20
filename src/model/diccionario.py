'''
   diccionary:
      Administra los accesos a datos del diccionario de una empresa cliente de Venaycia.com 

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from operator import itemgetter
from src.utility import xlsReader
from src.utility.validator import codeTransform
from src.mysqlConnector.diccionario import Diccionario
from src import db
import traceback

def getActivity(emp, act):
  '''
     getActivity: Crea los registro de un diccionario, asociaciados a una empresa \n
     @params: 
       company: id de la empresa a la que pertenece la actividad
       activity: Código de la actividad 'id_actividad'
  '''
  print("In getActivity:", act, emp)
  try:
    resp = Diccionario.query.filter(Diccionario.empresa == emp, Diccionario.id_actividad == act).first()
    if resp:
      return {'response': 'OK', 'data': resp.toJSON()}
    return {'response': 'ERROR', 'message': 'No se encontró la actividad ' + act}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un consultando la actividad ' + act}


def getDiccionarioByCompany(emp):
  '''
     getDiccionarioByCompany: Busca un diccionario de una empresa por su 'nit' \n
     @params:
       company: Id de la empresa a buscar en la DB
  '''
  print("In getDiccionarioByCompany:", emp)
  try:
    resp = []
    acts = Diccionario.query.filter(Diccionario.empresa == emp)
    for act in acts:
      resp.append(act.toJSON())
    if len(resp) > 0:
      return {'response': 'OK', 'data': resp}
    return {'response': 'ERROR', 'message': 'No se encontró el diccionario de la empresa ' + emp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Error de base de datos de diccionario'}

def addDiccionario(dicti, emp):
  '''
     addDiccionario: Crea los registro de un diccionario, asociaciados a una empresa \n
     @params: 
       dicti: objeto con los datos de los proceso de la compañia
       emp: id de la empresa a la que pertenece el diccionario
  '''
  print("In addDiccionario:", emp)
  try:
    lector = xlsReader.readXLS(dicti, 1)
    if 'ERROR' in lector:
      return {'response': 'ERROR', 'message': lector['ERROR']}
    valida = xlsReader.validateXLS(lector, ['nombre', 'nivel'])
    if 'ERROR' in valida:
      return {'response': 'ERROR', 'message': valida['ERROR'], 'data': valida['data']}
    lector = sorted(lector, key=itemgetter('nivel'))
    lista = []
    err   = []
    for dic in lector:
      dic['empresa'] = emp
      dic['padre'] = codeTransform(dic['padre'])
      dic['id_actividad'] = codeTransform(dic['id_actividad'])
      revisa = getActivity(dic['empresa'], dic['id_actividad'])
      if revisa['response'] != 'OK':
        if int(dic['nivel']) > 1:
          papa = getActivity(dic['empresa'], dic['padre'])
          if papa['response'] != 'OK':
            err.append({'response': papa['message'] + ' en la validación del padre', 'data': dic})
            dic.clear()
          else:
            papa = papa['data']
            dic['id_padre'] = papa['id']
        else:
          dic['id_padre'] = None
        if dic:
          resp = Diccionario(dic)
          db.session.add(resp)
          db.session.commit()
          lista.append(resp.toJSON())
      else:
        err.append({'response': 'Ya existe una actividad con ese id en la empresa', 'data': dic})
    return {'response': 'OK','data': lista, 'error': err}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error procesando el diccionario ' + dicti.filename}