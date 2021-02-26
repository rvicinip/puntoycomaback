### Se importan los plugins necesarios
from operator import itemgetter
from src.utility import xlsReader
from src.utility.validator import codeTransform
from src.mysqlConnector import diccionario
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
    resp = diccionario.query.filter(diccionario.empresa == emp, diccionario.id_actividad == act)
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un consultando la actividad ' + act}


def getDiccionarioByCompany(emp):
  '''
     getDiccionarioByCompany: Busca un diccionario de una empresa por su '_id' \n
     @params:
       company: Id de la empresa a buscar en la DB
  '''
  print("In getDiccionarioByCompany:", emp)
  try:
    resp = diccionario.query.filter(diccionario.empresa == emp)
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar la empresa: ' + emp}

def addDiccionario(dicti, emp):
  '''
     addDiccionario: Crea los registro de un diccionario, asociaciados a una empresa \n
     @params: 
       dicti: objeto con los datos de los proceso de la compañia
       emp: id de la empresa a la que pertenece el diccionario
       niveles: Cantidad de niveles que tiene el documento que se está guardando
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
        if dic:
          resp = diccionario.fromJSON(dic)
          db.session.add(resp)
          db.session.commit()
          lista.append(dic)
      else:
        err.append({'response': 'Ya existe una actividad con ese id en la empresa', 'data': dic})
    return {'response': 'OK','data': lista, 'error': err}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error procesando el diccionario ' + diccionario.filename}