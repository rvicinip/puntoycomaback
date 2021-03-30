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
from src.model import user, frecuencia, diccionario, empresa
from src.utility import xlsReader
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
    return {'response':'ERROR', 'message': 'Error de base de datos de encuesta'}

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
    return {'response': 'ERROR', 'message': 'Error de base de datos de encuesta'}

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
    return {'response': 'ERROR', 'message': 'No se encontró la respuesta a la encuesta: ' + str(idEnc)}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Error de base de datos de encuesta'}

def listSelectedActivities(usuario):
  '''
     listSelectedActivities: Lista las respuestas de la encuesta de un usuario en su reporte \n
     @params: 
       usuario: id_usuario del usuario asociado a la respuesta
  '''
  print("In listSelectedActivities")
  try:
    resp = []
    acts = Encuesta.query.filter(Encuesta.usuario == usuario, Encuesta.estado == 'A')
    for act in acts:
      resp.append(act.toJSON())
    if len(resp) > 0:
      return {'response': 'OK', 'data': resp}
    return {'response' : 'ERROR', 'message' : 'No se encontraron respuestas activas asociadas al usuario ' + str(usuario)}
  except Exception:
    traceback.print_exc()
    return {'response': 'OK', 'message': 'Error de base de datos de encuesta'}

def listEncuestaByCompany(company):
  '''
     listEncuestaByCompany: Lista las respuestas de las encuestas de los empleados de empresa \n
     @params: 
       company: Nit de la empresa
  '''
  print("In listEncuestaByCompany")
  try:
    resp = []
    empres = empresa.getCompanyByNIT(company)
    if not 'data' in empres:
      return empres
    empr = empres['data']
    empleados = user.getUsersByCompany(company)
    if not 'data' in empleados:
      return empleados
    emps = empleados['data']
    resp = []
    for emp in emps:
      dato = {}
      dato['id_usuario']   = emp['id_usuario']
      dato['nombre']       = emp['nombre']
      dato['salario']      = emp['salario']
      dato['jornada']      = emp['jornada']
      dato['cargo']        = emp['cargo']
      dato['tipocontrato'] = emp['tipocontrato']
      encuestas = listEncuestaByUsuario(emp['id_usuario'])
      if 'data' in encuestas:
        encs = encuestas['data']
        for enc in encs:
          dato['valorAct']   = enc['valorAct']
          dato['fteUsuario'] = enc['fteUser']
          dato['fteAct']     = enc['fteAct']
          dato['jornal']     = enc['jornada']
          dato['tiempo']     = enc['tiempo']
          dato['cantidad']   = enc['cantidad']
          umed = frecuencia.getFrecuenciaById(enc['umedida'])
          if 'data' in umed:
            umd = umed['data']
            dato['unidadtiempo'] = umd['nombre']
          else:
            return {'response': 'ERROR', 'message': 'Información Incompleta - NO se encontró la unidad de tiempo ' + str(enc['umedida'])}
          frec = frecuencia.getFrecuenciaById(enc['frecuencia'])
          if 'data' in frec:
            frc = frec['data']
            dato['frecuencia'] = frc['nombre']
          else:
            return {'response': 'ERROR', 'message': 'Información Incompleta - NO se encontró la frecuencia ' + str(enc['frecuencia'])}
          actividad = diccionario.getActivity(company, enc['actividad'])
          if 'data' in actividad:
            act = actividad['data']
            dato['tipo']         = act['tipo']
            dato['actividad']    = act['nombre']
            dato['mas']          = act['mas']
            dato['ceno']         = act['ceno']
            dato['cadenaValor']  = act['cadena_de_valor']            
            for i in range (int(empr['niveles'])-1):
              if act['id_padre'] > 0:
                padre = diccionario.getActivity(company, act['id_padre'])
                if 'data' in padre:
                  proc = padre['data']
                  dato['nivel' + str(int(empr['niveles']) - (i +1 ))] = proc['nombre']
                else:
                  return {'response': 'ERROR', 'message': 'Información Incompleta - NO se encontró la actividad ' + str(act['id_padre'])}
          else:
            return {'response': 'ERROR', 'message': 'Información Incompleta - NO se encontró la actividad ' + str(enc['actividad'])}
      else:
        return {'response': 'ERROR', 'message': 'Información Incompleta - NO se encontró encuesta para el empleador ' + str(emp['id_usuario'])}
      resp.append(dato)
    header = ['id_usuario', 'id_usuario', 'nombre', 'salario', 'jornada', 'cargo', 'tipocontrato', 'valorAct', 'fteUsuario',
              'fteAct', 'jornal', 'tiempo', 'cantidad', 'unidadtiempo', 'frecuencia', 'tipo', 'actividad', 'mas', 'ceno',
              'cadenaVr']
    for i in range (int(empr['niveles'])-1):
      header.append('nivel' + str(int(empr['niveles']) - (i +1 )))
    return {'response': 'OK', 'data': resp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Error de base de datos de encuesta'}

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
    return {'response': 'ERROR', 'message': 'Error de base de datos de encuesta'}

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
    return {'response': 'ERROR', 'message': 'Error de base de datos de encuesta'}

def countInquests(user):
  '''
     countInquests: Cuenta las respuestas de la encuesta del usuario que no tienen cantidad \n
     @params: 
        user: id_usuario que realiza la encuesta
  '''
  print("In countInquests")
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
    return {'response': 'ERROR', 'message': 'Error de base de datos de encuesta'}

def generateDesnomalizadaTable(company):
  '''
     generateDesnomalizadaTable: Genera los valores para construir la tabla desnomalizada que se descargará \n
     @params: 
       company: Nit de la empresa
  '''
  print('In generateDesnomalizadaTable:', company)
  header = ['id_usuario',	'nombre', 'salario', 'jornada',	'Cargo',	'tipo contrato',	'tipo',	
            'macro proceso', 'proceso', 'actividad', 'mas', 'ceno', 'tipo', 'cadenaVr',	'unidad tiempo',
            'frecuencia', 'cantidad',	'tiempo', 'jornada', 'fte actividad',	'fte usuario',	'valor act']
  table = listEncuestaByCompany(company)
  archivo = 'encuesta' + company + '.xlsx'
  xls = xlsReader.writeXLS(header, table, archivo)
  return xls

## ACTUALIZA
def updateSelectedActivity(encuesta):
  '''
     updateSelectedActivity: Actualiza una actividad agregando las respuesta de tiempo y frecuencia \n
     @params: 
       encuesta: Objeto Json de la encuesta seleccionada por el usuario
  '''
  try:
    print("In updateSelectedActivity")
    frec = frecuencia.getFrecuenciaById(encuesta['frecuencia'])
    if not 'data' in frec:
      return frec
    vrFrec = float(frec['data']['valor'])
    umed = frecuencia.getFrecuenciaById(encuesta['umedida'])
    if not 'data' in umed:
      return umed
    vrUmed = float(umed['data']['valor'])
    encuesta['tiempo'] = (float(encuesta['cantidad']) * vrUmed) / vrFrec
    verifica = getEncuestaById(encuesta['id'])
    if verifica['response'] == 'OK':
      value = verifica['data']
      if not str(value['usuario']) == str(encuesta['usuario']):
        return {'response': 'ERROR', 'message': 'El usuario ' + str(encuesta['usuario']) + ' no puede modificar esta encuesta'}
      resp = Encuesta.query.filter(Encuesta.id == encuesta['id']).update({
                                   Encuesta.cantidad   : encuesta['cantidad'],
                                   Encuesta.frecuencia : encuesta['frecuencia'],
                                   Encuesta.tiempo : encuesta['tiempo'],
                                   Encuesta.umedida    : encuesta['umedida']})
      db.session.commit()
      return {'response': 'OK', 'message': str(resp) + ' Respuesta actualizada'}
    return verifica
  except Exception:
    traceback.print_exc()
    return {'response':'ERROR', 'message': 'Error de base de datos de encuesta'}

def openInquest(idUser):
  '''
     openInquest: Abre la encuesta concluida de un usuario \n
     @params: 
       idUser: id_usuario del usuario a abrirle la encuesta
  '''
  try:
    print("In openInquest")
    resp = Encuesta.query.filter(Encuesta.usuario == idUser).update({Encuesta.estado : 'A'})
    db.session.commit()
    usu = user.statusInquest(idUser, "Desarrollo")
    if usu['response'] == 'ERROR':
      return usu
    return {'response': 'OK', 'message': str(resp) + ' Respuestas actualizadas'}
  except Exception:
    traceback.print_exc()
    return {'response':'ERROR', 'message': 'Error de base de datos de encuesta'}

def calculateIndices(usuario):
  '''
     calculateIndices: Actualiza las respuestas de un usuario calculando los valores de los indices \n
     @params: 
       usuario: ii_usuario que realiza la acción de cierre de encuesta
  '''
  try:
    print("In calculateIndices")
    usu = user.getUserByUsuario(usuario)
    if not 'data' in usu:
      return usu
    company = usu['data']['empresa']
    encuestas = listSelectedActivities(usuario)
    if not 'data' in encuestas:
      return encuestas
    encs = encuestas['data']
    jornada = float(0)
    for enc in encs:
      jornada += float(enc['tiempo'])
    jorEmpr = frecuencia.getFrecuencia(company, 'Dia', 1)
    if not 'data' in jorEmpr:
      return jorEmpr
    mesada = frecuencia.getFrecuencia(company, 'Mes', 1)
    if not 'data' in mesada:
      return mesada
    jEmp = int(jorEmpr['data']['valor'])
    mes  = int(mesada['data']['valor'])
    for e in encs:
      cant   = float(e['cantidad'])
      fteUsu = cant / jornada
      fteAct = cant / jEmp
      vrAct  = cant * (int(usu['data']['salario'])/mes)
      resp = Encuesta.query.filter(Encuesta.id == e['id']).update({
                                   Encuesta.fteAct   : fteAct,
                                   Encuesta.jornada  : jornada,
                                   Encuesta.fteUser  : fteUsu,
                                   Encuesta.valorAct : vrAct,
                                   Encuesta.estado   : 'T'})
      db.session.commit()
    return {'response': 'OK', 'message': ' Cálculos realizados correctamente'}
  except Exception:
    traceback.print_exc()
    return {'response':'ERROR', 'message': 'Error de base de datos de encuesta'}

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
    
    resp = Encuesta.query.filter(Encuesta.id == idActiv, Encuesta.usuario == idUser).first()
    if resp:
      db.session.delete(resp)
      db.session.commit()
      return {'response': 'OK', 'message': 'Encuesta eliminada correctamente'}
    return {'response': 'ERROR', 'message': 'NO se encuentra la encuesta ' + str(idActiv)}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Error de base de datos de encuesta'}
