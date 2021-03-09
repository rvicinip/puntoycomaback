'''
   frecuency:
      Administra los accesos a datos de las frecuencias de las empresas clientes de Venaycia.com 

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src.utility import xlsReader
from src.mysqlConnector.frecuencia import Frecuencia
from src import db
import traceback

def getFrecuencia(emp, nomb, tipo):
  '''
     getFrecuencia: Otiene una frecuencia acorde con los paramentros recibido \n
     @params: 
       company: id de la empresa a la que pertenece la actividad
       frecuency: Nombre de la frecuencia 'nombre'
       tipo: tipo de frecuencia (Unidad de Medida (1), Frecuencia (2))
  '''
  print("In getFrecuencia:", nomb, emp)
  try:
    resp = Frecuencia.query.filter(Frecuencia.nombre == nomb, 
                                   Frecuencia.empresa == emp,
                                   Frecuencia.tipo == tipo).first()
    if resp:
      return {'response' : 'OK', 'data': resp.toJSON()}
    return {'response' : 'ERROR', 'message' : 'No se encontró la frecuencia ' + nomb + ' para la empresa ' + str(emp)}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un consultando la actividad ' + nomb}

def getFrecuenciasByCompany(emp):
  '''
     getFrecuenciasByCompany: Busca las frecuencias de una empresa por su 'nit' \n
     @params:
       company: Id de la empresa a buscar en la DB 
  '''
  print("In getFrecuenciasByCompany:", emp)
  try:
    resp = []
    frecs = Frecuencia.query.filter(Frecuencia.empresa == emp)
    for frec in frecs:
      resp.append(frec.toJSON())
    if len(resp) > 0:
      return {'response': 'OK', 'data': resp}
    return {'response' : 'ERROR', 'message' : 'No se encontraron frecuencias para la empresa ' + emp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar la empresa: ' + emp}

def getFrecuenciaById(idFrec):
  '''
     getFrecuenciaById: Otiene una frecuencia por su id \n
     @params: 
       idFrec: Id de la frecuencia en la DB
  '''
  print("In getFrecuenciaById:", idFrec)
  try:
    resp = Frecuencia.query.filter(Frecuencia.id == idFrec).first()
    if resp:
      return {'response' : 'OK', 'data': resp.toJSON()}
    return {'response' : 'ERROR', 'message' : 'No se encontró la frecuencia ' + idFrec}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error consultando la frecuencia ' + idFrec}

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
        frec.clear()
      frec['valor'] = valor
      frec['tipo'] = int(frec['tipo'])
      revisa = getFrecuencia(frec['nombre'], frec['empresa'], frec['tipo'])
      if not revisa['response'] == 'OK':
        if frec:
          resp = Frecuencia(frec)
          db.session.add(resp)
          db.session.commit()
          lista.append(resp.toJSON())
      else:
        err.append({'response': 'Ya existe esta frecuencia en la empresa', 'data': frec})
    return {'response': 'OK', 'data': lista, 'error': err}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error procesando la frecuencia ' + frecs.filename}