'''
   encuesta

   Realiza las tareas necesarias para gestionar las respuestas de las preguntas por parte de los clientes

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from flask import jsonify, request
from src import app
from src.model import encuesta
from src.utility.validator import validateFields
from .protector import privated

@app.route('/inquest/select', methods = ['POST'])
@privated
def createUserActivities(usuario):
  '''
     createUserActivities: Crea las actividades del usuario para empezar las respuestas de reporte de tiempos \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente
  '''
  print("In createUserActivities")
  campos = ['actividades']
  datos = request.json
  valida = validateFields(campos, datos)
  if valida['response'] == 'ERROR':
    return jsonify(valida)
  cliente = usuario['_id']
  acts = datos['actividades']
  resp = encuesta.createSelectedActivity(cliente, acts)
  return jsonify(resp)

@app.route('/inquest/answer', methods = ['POST'])
@privated
def updateUserActivities(usuario):
  '''
     updateUserActivities: Actualiza las actividades del usuario guardando las respuestas de reporte de tiempos \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente
  '''
  print("In updateUserActivities")
  campos = ['actividades']
  datos = request.json
  valida = validateFields(campos, datos)
  if valida['response'] == 'ERROR':
    return jsonify(valida)
  cliente = usuario['_id']
  acts = datos['actividades']
  vals = acts[0]
  if vals['cliente'] != usuario['_id']:
      return jsonify({'response':'ERROR', 'message': 'El usuario no coincide'})
  resp = encuesta.createSelectedActivity(cliente, acts)
  return jsonify(resp)

@app.route('/inquest/list', methods = ['GET'])
@privated
def listUserActivities(usuario):
  '''
     listUserActivities: Lista las actividades del usuario con las respuestas de reporte de tiempos \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente
  '''
  print("In updateUserActivities")
  cliente = usuario['_id']
  resp = encuesta.listSelectedActivities(cliente)
  return jsonify(resp)