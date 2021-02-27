'''
   encuesta

   Gestiona en la DB las respuestas de las preguntas por parte de los clientes

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src.mongoCRUD import connector
from src.utility.validator import validateFields
from config import MONGO, DB
from bson import ObjectId
import traceback

ENCCOLL = 'encuesta'

def createSelectedActivity(actividad):
  '''
     selectActivity: Crea una actividad en la lista de un usuario \n
     @params: 
       actividad: Objeto Json de la actividad seleccionada por el usuario
  '''
  try:
    resp = connector.addToCollection(MONGO, DB, ENCCOLL, actividad)
    if not ObjectId.is_valid(str(resp)):
      return {'response': 'ERROR', 'message': resp['ERROR']}
    actividad['id'] = str(ObjectId(resp))
    return {'response': 'OK', 'message': 'Encuesta de usuario creada', 'data': actividad}
  except Exception:
    traceback.print_exc()
    return {'response':'ERROR', 'message': 'Se presentó un error al crear la encuesta'}

def createSelectedActivities(usuario, actividades):
  '''
     selectActivities: Crea la lista de actividades seleccionadas por un usuario para su reporte \n
     @params: 
       usuario: Id mongo del usuario asociado a la actividad
       actividades: Lista de Id mongo de la actividades seleccionadas por el usuario
  '''
  resp = []
  encuesta = {}
  encuesta['cliente'] = usuario
  for act in actividades:
    encuesta['actividad'] = act
    crea = createSelectedActivity(encuesta)
    if not 'data' in crea:
        return crea
    resp.append(crea['data'])
  return {'response': 'OK', 'data': resp}

def updateSelectedActivity(actividad):
  '''
     updateSelectedActivity: Actualiza una actividad agregando las respuesta de tiempo y frecuencia \n
     @params: 
       actividad: Objeto Json de la actividad seleccionada por el usuario
  '''
  try:
    resp = connector.updateById(MONGO, DB, ENCCOLL, actividad)
    if not resp.acknowledged:
        return {'response': 'ERROR', 'message': 'No se actualizó la actividad'}
    return {'response': 'OK', 'message': 'Actividad actualizada', 'data': actividad}
  except Exception:
    traceback.print_exc()
    return {'response':'ERROR', 'message': 'Se presentó un error actualziando la actividad'}

def updateSelectedActivities(usuario, actividades):
  '''
     updateSelectedActivities: Actualiza la lista de respuesta de las actividades de un usuario en su reporte \n
     @params: 
       usuario: Id mongo del usuario asociado a la actividad
       actividades: Lista de objetos Json de las actividades con respuesta por el usuario
  '''
  campos = ['id', 'cliente', 'actividad', 'tiempo', 'frecuencia']
  acts = []
  fallo = []
  for data in actividades:
    valida = validateFields(campos, data)
    if valida['response'] == 'ERROR':
      data['message'] = valida['message']
      fallo.append(data)
    else:
      modifica = updateSelectedActivity(data)
      if not 'data' in modifica:
        data['message'] = modifica['message']
        fallo.append(data)
      else:
        acts.append(data)
  return {'response': 'OK', 'fallo': fallo, 'data': acts}

def listSelectedActivities(usuario):
  '''
     listSelectedActivities: Lista las respuestas de las actividades de un usuario en su reporte \n
     @params: 
       usuario: Id mongo del usuario asociado a la actividad
  '''
  try:
    resp = connector.getCollecctionsByField(MONGO, DB, ENCCOLL, {'cliente': usuario})
    if 'ERROR' in resp:
      return {'response': 'ERROR', 'message': resp['ERROR']}
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'OK', 'message': 'Se presentó un error al consultar la encuesta del usuario ' + usuario}