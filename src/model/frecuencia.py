### Se importan los plugins necesarios
from src.utility import xlsReader
from src.mysqlConnector import frecuencia
from src import db
import traceback

def getFrecuencia(emp, frec):
  '''
     getFrecuencia: Crea los registro de un diccionario, asociaciados a una empresa \n
     @params: 
       company: id de la empresa a la que pertenece la actividad
       frecuency: Nombre de la frecuencia 'nombre'
  '''
  print("In getFrecuencia:", frec, emp)
  try:
    resp = frecuencia.query.filter(frecuencia.nombre == frec, frecuencia.empresa == emp)
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un consultando la actividad ' + frec}

def getFrecuenciasByCompany(emp):
  '''
     getFrecuenciasByCompany: Busca las frecuencias de una empresa por su '_id' \n
     @params:
       company: Id de la empresa a buscar en la DB 
  '''
  print("In getFrecuenciasByCompany:", emp)
  try:
    resp = frecuencia.query.filter(frecuencia.empresa == emp)
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar la empresa: ' + emp}

def addFrecuacia(frecs, emp):
  '''
     addFrecuacia: Crea los registro de un diccionario, asociaciados a una empresa \n
     @params: 
       frecuencia: objeto con los datos de los tiempos y frecuencias de la compañia
       company: id mongo de la empresa a la que pertenecen las frecuencias
  '''
  print("In addFrecuacia:", emp)
  try:
    lector = xlsReader.readXLS(frecs, 1)
    if 'ERROR' in lector:
      return {'response': 'ERROR', 'message': lector['ERROR']}
    valida = xlsReader.validateXLS(lector, ['nombre',	'tipo',	'valor'])
    if 'ERROR' in valida:
      return {'response': 'ERROR', 'message': valida['ERROR'], 'data': valida['data']}
    lista = []
    err   = []
    for frec in lector:
      frec['empresa'] = emp
      valor = float(frec['valor'])
      if valor <= 0 :
        err.append({'response': 'el valor de la frecuencia debe ser mayor a 0', 'data': frec})
        frec = {}
      frec['valor'] = valor
      frec['tipo'] = int(frec['tipo'])
      revisa = getFrecuencia(frec['nombre'], frec['empresa'])
      if revisa['response'] != 'OK':
        resp = frecuencia.fromJSON(frec)
        db.session.add(resp)
        db.session.commit()
        lista.append(resp)
      else:
        err.append({'response': 'Ya existe esta frecuencia en la empresa', 'data': frec})
    return {'response': 'OK', 'data': lista, 'error': err}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error procesando la frecuencia ' + frecs.filename}