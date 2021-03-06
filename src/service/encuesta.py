'''
   encuesta:
      Administra los servicios de las respuestas a la encuesta por parte de los clientes

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from flask import jsonify, request
from src import app
from src.model import encuesta
from src.model import user
from src.utility.mailer import sendMail
from src.utility.validator import validateFields
from .protector import privated

@app.route('/coount/<user>', methods = ['GET'])
def contador(user):
  '''
     contador: Crea las actividades del usuario para empezar las respuestas de reporte de tiempos \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente (Se obtiene del token)
  '''
  print("In contador")
  resp = encuesta.countAnswers(user)
  print("End contador:", resp)
  return jsonify(resp)

@app.route('/inquest/answer', methods = ['POST'])
@privated
def createUserActivity(usuario):
  '''
     createUserActivity: Crea las actividades del usuario para empezar las respuestas de reporte de tiempos \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente (Se obtiene del token)
  '''
  print("In createUserActivity")
  campos = ['actividad', 'frecuencia', 'cantidad', 'umedida']
  datos = request.json
  valida = validateFields(campos, datos)
  if valida['response'] == 'ERROR':
    return jsonify(valida)
  datos['usuario'] = usuario['id_usuario']
  valor = encuesta.getEncuestaByUser(datos['actividad'], datos['usuario'])
  if 'data' in valor:
    c = int(valor['data']['cantidad']) 
    if c > 0 :
      return jsonify({'response':'ERROR', 'message': 'Ya existe esta actividad para el usuario con cantidad ' + str(c)})
    return jsonify({'response':'ERROR', 'message': 'Ya existe esta actividad para el usuario'})
  resp = encuesta.createSelectedActivity(datos)
  print("End createUserActivity: ", resp)
  return jsonify(resp)

@app.route('/inquest', methods = ['POST'])
@privated
def createEncuesta(usuario):
  '''
     createEncuesta: Crea las actividades seleccionadas por el usuario creando la encuesta de reporte de tiempos \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente (Se obtiene del token)
  '''
  print("In createEncuesta")
  campos = ['actividad']
  datos = request.json
  valida = validateFields(campos, datos)
  if valida['response'] == 'ERROR':
    return jsonify(valida)
  datos['usuario']   = usuario['id_usuario']
  datos['cantidad']  = 0
  valor = encuesta.getEncuestaByUser(datos['actividad'], datos['usuario'])
  if 'data' in valor:
    if int(valor['data']['cantidad']) > 0 :
      return jsonify({'response':'ERROR', 'message': 'Ya existe esta actividad para el usuario con cantidad ' + str(valor['data']['cantidad'])})
    return jsonify({'response':'ERROR', 'message': 'Ya existe esta actividad para el usuario'})
  resp = encuesta.createSelectedActivity(datos)
  print("End createEncuesta:", resp)
  return jsonify(resp)

@app.route('/inquest/answer', methods = ['PUT'])
@privated
def updateUserActivity(usuario):
  '''
     updateUserActivity: Actualiza las actividades del usuario guardando las respuestas de reporte de tiempos \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente (Se obtiene del token)
  '''
  print("In updateUserActivity")
  campos = ['actividad', 'frecuencia', 'cantidad', 'umedida']
  datos = request.json
  valida = validateFields(campos, datos)
  if valida['response'] == 'ERROR':
    return jsonify(valida)
  if not str(datos['usuario']) == str(usuario['id_usuario']):
      return jsonify({'response':'ERROR', 'message': 'El usuario logueado no tiene permisos para modificar esta respuesta'})
  resp = encuesta.updateSelectedActivity(datos)
  print("End updateUserActivity:", resp)
  return jsonify(resp)

@app.route('/inquest/list', methods = ['GET'])
@privated
def listUserActivities(usuario):
  '''
     listUserActivities: Lista las actividades del usuario con las respuestas de reporte de tiempos \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente (Se obtiene del token)
  '''
  print("In listUserActivities")
  cliente = usuario['id_usuario']
  resp = encuesta.listEncuestaByUsuario(cliente)
  print("End listUserActivities:", resp)
  return jsonify(resp)

@app.route('/inquest/list/<id_usuario>', methods = ['GET'])
@privated
def listActivitiesByUser(usuario, id_usuario):
  '''
     listActivitiesByUser: Lista las actividades de un usuario con las respuestas de reporte de tiempos \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente (Se obtiene del token)
       id_usuario: id del usuario al cual se le consultarán las actividades
  '''
  print("In listActivitiesByUser")
  if usuario['perfil'] == 'client':
    return jsonify({'response': 'ERROR', 'message': "El usuario no tiene privilegios para realizar esta acción"})
  resp = encuesta.listEncuestaByUsuario(id_usuario)
  print("End listActivitiesByUser:", resp)
  return jsonify(resp)

@app.route('/inquest/<actividad>', methods = ['DELETE'])
@privated
def deleteActivity(usuario, actividad):
  '''
     deleteActivity: Elimina una respuesta de la encuesta \n
     @params:
       actividad: Id de la actividad a borrar
  '''
  print("In deleteActivity:", actividad)
  resp = encuesta.deleteEncuestaById(actividad, usuario['id_usuario'])
  print("End deleteActivity:", resp)
  return jsonify(resp)

@app.route('/inquest/close', methods = ['GET'])
@privated
def closeInquest(usuario):
  '''
     closeInquest: cierra la encuesta de un usuario \n
  '''
  print("In closeInquest")
  resp = user.closeUserInquest(usuario['id_usuario'])
  print("End closeInquest:", resp)
  return jsonify(resp)

@app.route('/export/inquest', methods = ['POST'])
@privated
def generateTable(usuario):
  '''
     generateTable: Lista las actividades del usuario con las respuestas de reporte de tiempos y la exporta en un XLS \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente (Se obtiene del token)
  '''
  print("In generateTable")
  ## Validad que se enviarion todos los campos
  dato = request.json
  campos = ['empresa']
  valida = validateFields(campos, dato)
  if valida['response'] == 'ERROR':
    return jsonify(valida)
  resp = encuesta.generateDesnomalizadaTable(dato['empresa'])
  print("End generateTable:", resp)
  return jsonify(resp)

@app.route('/inquest/open', methods = ['POST'])
@privated
def openInquest(usuario):
  '''
     openInquest: Abre la encuesta de un usuario que ya había terminado el resporte \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente (Se obtiene del token)
  '''
  print("In openInquest")
  ## Validad que se enviarion todos los campos
  dato = request.json
  campos = ['usuario']
  valida = validateFields(campos, dato)
  if valida['response'] == 'ERROR':
    return jsonify(valida)
  resp = encuesta.openInquest(dato['usuario'])
  print("End openInquest:", resp)
  return jsonify(resp)

@app.route('/remember', methods = ['POST'])
@privated
def rememberInquest(usuario):
  '''
     rememberInquest: Envia correo de recordando diligenciar la encuesta \n
     @params:
       usuario: Objeto Json con los datos del usuario cliente (Se obtiene del token)
  '''
  print("In rememberInquest")
  ## Validad que se enviarion todos los campos
  dato = request.json
  campos = ['usuario']
  mensaje = "Vena lo invita a realizar el reporte de las actividades. Su compromiso nos permite realizar el estudio y generar información verídica para la empresa"
  valida = validateFields(campos, dato)
  if valida['response'] == 'ERROR':
    return jsonify(valida)
  usuario = user.getUserByUsuario(dato['usuario'])
  if usuario['response'] == 'ERROR':
    return jsonify(usuario)
  mail = usuario['data']['email']
  resp = sendMail(mail, mensaje)
  print("End rememberInquest:", resp)
  return jsonify(resp)