'''
   encuesta:
      Administra los accesos a datos de las respuestas a la encuesta por parte de los clientes

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src.utility.validator import validateFields
from src.mysqlConnector.encuesta import Encuesta
from src.mysqlConnector.frecuencia import Frecuencia
from src.mysqlConnector.diccionario import Diccionario
from src.model import user
from src import db
import traceback

# Métodos CRUD en las coleeciones diccionario, empresa y frecuencias
### CREA
def createSelectedActivity(activity):
  '''
     selectActivity: Crea una actividad en la lista de un usuario \n
     @params: 
       actividad: Objeto Json de la actividad seleccionada por el usuario
  '''
  try:
    valida = countAnswers(activity['usuario'])
    if not 'data' in valida:
      iniciar = user.statusInquest(activity['usuario'], 'Desarrollo')
      if iniciar['response'] == 'ERROR':
        return iniciar
    actividad = Encuesta(activity)
    db.session.add(actividad)
    db.session.commit()
    return {'response': 'OK', 'message': 'Respuesta de encuesta creada', 'data': {'encuesta': actividad.toJSON()}}    
  except Exception:
    traceback.print_exc()
    return {'response':'ERROR', 'message': 'Se presentó un error al crear la encuesta'}

### LEE
def getEncuestaByUser(idAct, idUser):
  '''
     getEncuestaByUser: Busca respuestas a la encuesta en la DB por el campo id_actividad \n
     @params:
       idAct: Id de actividae al a buscar en la DB 
       idUser: id_usuario con el que está asociada la respuesta
  '''
  print("In getEncuestaByUser:", idAct)
  try:
    resp = Encuesta.query.filter(Encuesta.actividad == idAct, Encuesta.usuario == idUser).first()
    if resp:
      return {'response': 'OK', 'data': resp.toJSON()}
    return {'response': 'ERROR', 'message': 'No se encontró la respuesta a la encuesta ' + str(idUser)}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + str(idUser)}

def getEncuestaById(idEnc):
  '''
     getEncuestaById: Busca una respuesta a la encuesta en la DB \n
     @params:
       idAct: Id de respuesta de la encuesta a buscar en la DB 
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

def listSelectedActivities(usuario):
  '''
     listSelectedActivities: Lista las respuestas de la encuesta de un usuario en su reporte \n
     @params: 
       usuario: id_usuario del usuario asociado a la respuesta
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

def listEncuestaByUsuariOld(usuario):
  '''
     listEncuestaByUsuario: Lista las respuestas de la encuesta de un usuario en su reporte \n
     @params: 
       usuario: id_usuario del usuario asociado a la respuesta
  '''
  print("In listEncuestaByUsuario")
  try:
    encs = db.session.query(
      Encuesta,
      Diccionario.nombre,
      Diccionario.id_actividad,
      Diccionario.descripcion,
      Frecuencia.nombre).select_from(
        Encuesta, 
        Frecuencia, 
        Diccionario).filter(
          Encuesta.usuario == usuario,
          Diccionario.id == Encuesta.actividad,
          Frecuencia.id == Encuesta.frecuencia)
    resp = []
    for enc in encs:
      umed = Frecuencia.query.filter(Frecuencia.id == enc[0].umedida).first()
      e = {}
      e['Encuesta']    = enc[0].toJSON()
      e['frecuencia']  = enc[4]
      e['umedida']     = umed.nombre
      e['diccionario'] = {'nombre'       : enc[1],
                          'id_actividad' : enc[2],
                          'descripcion'  : enc[3]}
      resp.append(e)
    if len(resp) > 0:
      return {'response': 'OK', 'data': resp}
    return {'response' : 'ERROR', 'message' : 'No se encontraron actividades asociadas al usuario ' + str(usuario)}
  except Exception:
    traceback.print_exc()
    return {'response': 'OK', 'message': 'Se presentó un error al consultar la encuesta del usuario ' + str(usuario)}

def listEncuestaByUsuario(usuario):
  '''
     listEncuestaByUsuario: Lista las respuestas de la encuesta de un usuario en su reporte \n
     @params: 
       usuario: id_usuario del usuario asociado a la respuesta
  '''
  print("In listEncuestaByUsuario")
  try:
    encuestas = db.session.query(
                Encuesta,
                Diccionario.nombre,
                Diccionario.id_actividad,
                Diccionario.descripcion).select_from(
                  Encuesta, 
                  Diccionario).filter(
                    Encuesta.usuario == usuario,
                    Diccionario.id == Encuesta.actividad)
    resp = []
    for enc in encuestas:
      e = {}
      e['frecuencia'] = None
      e['umedida'] = None
      encuesta = enc[0].toJSON()
      if encuesta['frecuencia'] is not None:
        frec = Frecuencia.query.filter(Frecuencia.id == encuesta['frecuencia']).first()
        e['frecuencia'] = frec.nombre
      if encuesta['umedida'] is not None:
        umed = Frecuencia.query.filter(Frecuencia.id == encuesta['umedida']).first()
        e['umedida'] = umed.nombre
      e['encuesta']    = encuesta
      e['diccionario'] = {'nombre'       : enc[1],
                          'id_actividad' : enc[2],
                          'descripcion'  : enc[3]}
      resp.append(e)
    if len(resp) > 0:
      return {'response': 'OK', 'data': resp}
    return {'response' : 'ERROR', 'message' : 'No se encontraron actividades asociadas al usuario ' + str(usuario)}
  except Exception:
    traceback.print_exc()
    return {'response': 'OK', 'message': 'Se presentó un error al consultar la encuesta del usuario ' + str(usuario)}

def countAnswers(idUser):
  '''
     countAnswers: Cuenta las respuesta que tiene un usuario \n
     @params:
       idUser: id_usuario con el que está asociada la respuesta
  '''
  print("In countAnswers:", idUser)
  try:
    resp = Encuesta.query.filter(Encuesta.usuario == idUser).count()
    if resp > 0:
      return {'response': 'OK', 'data': resp}
    return {'response': 'ERROR', 'message': 'No se encontraron resultados'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + str(idUser)}

def countInquests(user):
  '''
     closeInquest: Cuenta las respuestas de la encuesta del usuario que no tienen cantidad \n
     @params: 
        user: id_usuario que realiza la encuesta
  '''
  print("In closeInquest")
  try:
    resp = {}
    encs = Encuesta.query.filter(Encuesta.usuario == user)
    pend = 0
    tot  = 0
    for enc in encs:
      tot += 1
      if enc.cantidad <= 0:
        pend += 1
    resp['pendiente'] = pend
    resp['total']     = tot
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar las respuestas de ' + str(user)}

## ACTUALIZA
def updateSelectedActivity(encuesta):
  '''
     updateSelectedActivity: Actualiza una actividad agregando las respuesta de tiempo y frecuencia \n
     @params: 
       encuesta: Objeto Json de la encuesta seleccionada por el usuario
  '''
  try:
    verifica = getEncuestaById(encuesta['actividad'])
    if verifica['response'] == 'OK':
      value = verifica['data']
      if value['usuario'] != encuesta['usuario']:
        return {'response': 'ERROR', 'message': 'El usuario ' + str(encuesta['usuario']) + ' no puede modificar esta encuesta'}
      resp = Encuesta.query.filter(Encuesta.actividad == encuesta['actividad'], Encuesta.usuario == encuesta['usuario']).update({
                                   Encuesta.cantidad   : encuesta['cantidad'],
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

### ELIMINA
def deleteEncuestaById(idActiv, idUser):
  '''
     deleteEncuestaById: Elimina una respuesta a la encuesta de la DB \n
     @params: 
       idActiv: Id de la actividad en la respuesta de la encuesta a eliminar en la DB 
       idUser: id_usuario de usuario que realiza la respuesta
  '''
  print("In deleteEncuestaById:", idActiv)
  try:
    resp = Encuesta.query.filter(Encuesta.actividad == idActiv, Encuesta.usuario == idUser).first()
    db.session.delete(resp)
    db.session.commit()
    return {'response': 'OK', 'message': 'Encuesta eliminada correctamente'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al eliminar la respuesta de la actividad: ' + str(idActiv)}
