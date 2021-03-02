'''
   encuesta

   Gestiona en la DB las respuestas de las preguntas por parte de los clientes

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src.utility.validator import validateFields
from src.mysqlConnector.encuesta import Encuesta
from src import db
import traceback

def createSelectedActivity(activity):
  '''
     selectActivity: Crea una actividad en la lista de un usuario \n
     @params: 
       actividad: Objeto Json de la actividad seleccionada por el usuario
  '''
  try:
    actividad = Encuesta(activity)
    db.session.add(actividad)
    db.session.commit()
    return {'response': 'OK', 'message': 'Respuesta de encuesta creada'}    
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
  encuesta['usuario'] = usuario
  for act in actividades:
    encuesta['actividad'] = act
    crea = createSelectedActivity(encuesta)
    if not 'data' in crea:
        return crea
    resp.append(crea['data'])
  return {'response': 'OK', 'data': resp}

def getEncuestaById(idEnc):
  '''
     getEncuestaById: Busca una empresa en la coleeción de empresas por el 'nit' \n
     @params:
       idAct: Id de actividad a buscar en la DB 
  '''
  print("In getEncuestaById:", idEnc)
  try:
    resp = Encuesta.query.filter(Encuesta.id == idEnc, Encuesta.estado == 'A').first()
    if resp:
      return {'response': 'OK', 'data': resp.toJSON()}
    return {'response': 'ERROR', 'message': 'No se encontró la respuesta a la encuesta ' + str(idEnc)}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + str(idEnc)}

def updateSelectedActivity(encuesta):
  '''
     updateSelectedActivity: Actualiza una actividad agregando las respuesta de tiempo y frecuencia \n
     @params: 
       encuesta: Objeto Json de la encuesta seleccionada por el usuario
  '''
  try:
    verifica = getEncuestaById(encuesta['id'])
    if verifica['response'] == 'OK':
      value = verifica['data']
      if value['usuario'] != encuesta['usuario']:
        return {'response': 'ERROR', 'message': 'El usuario ' + str(encuesta['usuario']) + ' no puede modificar esta encuesta'}
      resp = Encuesta.query.filter(Encuesta.id == encuesta['id']).update({
                                  Encuesta.actividad  : encuesta['actividad'],
                                  Encuesta.tiempo     : encuesta['tiempo'],
                                  Encuesta.frecuencia : encuesta['frecuencia'],
                                  Encuesta.umedida    : encuesta['umedida']})
      db.session.commit()
      return {'response': 'OK', 'message': str(resp) + ' Encuesta actualizada'}
    return {'response': 'ERROR', 'message': 'No se existe la encuesta' + str(encuesta['id'])}
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
       usuario: id_usuario del usuario asociado a la actividad
  '''
  print("In listSelectedActivities")
  try:
    resp = []
    acts = Encuesta.query.filter(Encuesta.usuario == usuario)
    for act in acts:
      resp.append(act.toJSON())
    if len(resp) > 0:
      return {'response': 'OK', 'data': resp}
    return {'response' : 'ERROR', 'message' : 'No se encontraron actividades asociadas al usuario ' + str(usuario)}
  except Exception:
    traceback.print_exc()
    return {'response': 'OK', 'message': 'Se presentó un error al consultar la encuesta del usuario ' + str(usuario)}

### ELIMINA
def deleteEncuestaById(idEnc):
  '''
     deleteEncuestaById: Elimina una respuesta a la encuesta de la DB \n
     @params: 
       idEnc: Id de la respuesta de la encuesta a eliminar en la DB 
  '''
  print("In deleteEncuestaById:", idEnc)
  try:
    resp = Encuesta.query.filter(Encuesta.id == idEnc).first()
    db.session.delete(resp)
    db.session.commit()
    return {'response': 'OK', 'message': 'Encuesta eliminada correctamente'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al eliminar el usuario: ' + str(idEnc)}
