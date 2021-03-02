'''
   user:
      Administra los accesos a datos a la colección de usuario donde se guardan los datos de los usuarios del sistema

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Vitt Inversiones SAS - vitt.co
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from random import randint
from src.utility import mailer
from src.mysqlConnector.usuario import Usuario
from src.utility import xlsReader
from src import db
import bcrypt
import traceback

# Métodos CRUD en la coleeción usuario
### CREA
def addUserClient(user, empresa):
  '''
     addUser: Crea un usuario en la colección de usaurio \n
     @params: 
       usuario: objeto Json con los campos a insertar en la DB 
       empresa: Id mongo de la empresa a la que se asocia el usuario a crear
  '''
  print("In addUserClient:", empresa)
  user['salario'] = int(user['salario'])
  user['empresa'] = empresa
  user['perfil'] = 'client'
  user['estado'] = 'A' ## A indica que el estado del usuario es activo
  clave = str(user['clave']).encode()
  encripted = bcrypt.hashpw(clave, bcrypt.gensalt(12))
  user['clave'] = encripted.decode('utf-8')
  try:
    verifica = getUserByUsuario(user['id_usuario'])
    if not 'data' in verifica:
      info = Usuario(user)
      db.session.add(info)
      db.session.commit()
      return {'response': 'OK', 'message': 'Usuario creado correctamente', 'data' : info.toJSON()}
    return {'response': 'ERROR', 'message': 'Ya existe un usuario con el mismo id'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}

def addUserEmpresa(user):
  '''
     addUserEmpresa: Crea un usuario consultor en la colección de usaurio \n
     @params: 
       usuario: objeto Json con los campos a insertar en la DB 
       empresa: Id mongo de la empresa a la que se asocia el usuario a crear
  '''
  print("In addUserEmpresa")
  if 'salario' in user:
    user['salario'] = int(user['salario'])
  user['perfil'] = 'consult'
  user['estado'] = 'A' ## A indica que el estado del usuario es activo
  clave = str(user['clave']).encode()
  encripted = bcrypt.hashpw(clave, bcrypt.gensalt(12))
  user['clave'] = encripted.decode('utf-8')
  try:
    usu = Usuario(user)
    print("addUserEmpresa - usu", usu)
    verifica = getUserByUsuario(user['id_usuario'])
    print("addUserEmpresa - verifica", verifica)
    if not 'data' in verifica:
      db.session.add(usu)
      db.session.commit()
      return {'response': 'OK', 'message': 'Usuario creado correctamente'}
    return {'response': 'ERROR', 'message': 'Ya existe el usuario', 'data': verifica['data']}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al crear el usuario'}

def addEmpleados(user, idEmp):
  '''
     addEmpleados: Crea los registro de los empleados asociaciados a una empresa \n
     @params: 
       usuario: objeto con los datos de los empleados de la compañia
       idEmp: id mongo de la empresa a la que pertenecen los usuarios
  '''
  print("In addEmpleados:", idEmp)
  try:
    lector = xlsReader.readXLS(user, 1) ## Archivo, Hojas a leer
    if 'ERROR' in lector:
      return {'response': 'ERROR', 'message': lector['ERROR']}
    campos = ['id_usuario',	'clave',	'nombre',	'salario',	'jornada',	'cargo',	'tipo']
    valida = xlsReader.validateXLS(lector, campos)
    if 'ERROR' in valida:
      return {'response': 'ERROR', 'message': valida['ERROR'], 'data': valida['data']}
    lista = []
    err   = []
    for usu in lector:
      resp = addUserClient(usu, idEmp)
      if resp['response'] == 'ERROR':
        err.append({'response': resp['message'], 'data': usu})
      else:
        lista.append(resp['data'])
    return {'response': 'OK', 'data': lista, 'error': err}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error procesando los empleados ' + user.filename}

### LEE
def getUserByUsuario(idUser):
  '''
     getUserByUsuario: Busca un usuario en la coleeción de usaurio por el 'id_usuario' \n
     @params: 
       idUser: Id del objeto usuario a buscar en la DB 
  '''
  print("In getUserByUsuario:", idUser)
  try:
    resp = Usuario.query.filter(Usuario.id_usuario == idUser).first()
    if resp:
      return {'response': 'OK', 'data': resp.toJSON()}
    return {'response': 'ERROR', 'message': 'No se encontró el usuario ' + str(idUser)}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + str(idUser)}

def getUsersByCompany(idCompany):
  '''
     getUsersByCompany: Busca todos los usuario de una empresa en la coleeción de usaurio \n
     @params: 
       idCompany: Id mongo de la empresa a la que está asociado el usuario en la DB 
  '''
  print("In getUsersByCompany:", idCompany)
  try:
    usus = Usuario.query.filter(Usuario.empresa == idCompany, Usuario.estado == 'A')
    resp = []
    for us in usus:
      resp.append(us.toJSON())
    if len(resp) > 0:
      return {'response': 'OK', 'data': resp}
    return {'response': 'ERROR', 'message': 'No se encuentras empleados para la empresa ' + str(idCompany)}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar los usuarios de la empresa: ' + str(idCompany)}

def recallUserPassword(idUsuario):
  '''
     recallUserPassword: genera y envía un código para recuperar la contraseña de una cuenta \n
     @params: 
        idUsuario: nombre de usuario 'id_usuario' del cliente a recuperar contraseña
  '''
  print("In recallUserPassword:", idUsuario)
  try:
    resp = getUserByUsuario(idUsuario)
    if resp['response'] == 'ERROR':
      return resp
    urc = resp['data']
    if urc['email'] == '':
      return {'response': 'NOMAIL', 'data': urc}
    codigo = randint(100000, 999999)
    mensaje = 'Para el cambio de la clave de seguiridad tu cuenta, por favor confirme con el siguente codigo ' + str(codigo)
    urc['codigo'] = int(codigo)
    upd = updateUserById(urc)
    if upd['response'] == 'OK':
      valida = upd['data']  
      mail = mailer.sendMail(valida['email'], mensaje)
      if mail['response'] == 'OK':
        return {'response': 'OK', 'message': 'correo enviado a ' + valida['email']}
      return mail
    return upd
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar el usuario: ' + str(idUsuario)}

def validateCodigo(user):
  '''
     validateCodigo: Valida que código corresponda con el enviado al usuario y habilita el cambio de contraseña \n
     @params: 
        usuario: objeto Json con los datos de usuario para validar 'id_usuario', 'nueva_clave' y 'codigo' 
  '''
  print("In validateCodigo:", user['id_usuario'])
  try:
    datos = getUserByUsuario(user['id_usuario'])
    if datos['response'] == 'OK':
      values = datos['data']
      print('values', values, 'usuario', user['codigo'])
      if int(values['codigo']) == int(user['codigo']):
        user['id_usuario'] = values['id_usuario']
        return updatePasswordByCodigo(user)
      return {'response':'ERROR', 'message':'El código no concuerda'}
    return datos
  except Exception:
    traceback.print_exc()
    return {'response':'ERROR', 'message':'Se presentó un error validando el código del usuario'}

def validatePassword(user):
  '''
     validatePassword: Valida que la contraseña corresponda con el usuario en la DB \n
     @params: 
        user: objeto Json con los datos de usuario para validar en la DB, sólo toma 'id_usuario' y 'clave' 
  '''
  print("In validatePassword:", user['id_usuario'])
  try:
    verifica = getUserByUsuario(user['id_usuario'])
    us = verifica['data']
    if bcrypt.checkpw(str(user['clave']).encode(), str(us['clave']).encode()):
      return {'response':'OK', 'data': us}
    return {'response':'ERROR', 'message':'Contraseña errada'}
  except Exception:
    traceback.print_exc()
    return {'response':'ERROR', 'message':'Se presentó un error validando el usuario'}

### ACTUALIZA
def updateUserById(user):
  '''
     updateUserById: Actualiza un usuario en la colección de usaurio \n
     @params:
       usuario: objeto usuario con todos los datos a modificar en la DB 
  '''
  print("In updateUserById:", user['id_usuario'])
  try:
    resp = Usuario.query.filter(Usuario.id_usuario == user['id_usuario']).update({
           Usuario.nombre     : user['nombre'],
           Usuario.empresa    : user['empresa'],
           Usuario.email      : user['email'],
           Usuario.cargo      : user['cargo'],
           Usuario.salario    : user['salario'],
           Usuario.jornada    : user['jornada'],
           Usuario.perfil     : user['perfil'],
           Usuario.ccostos    : user['ccostos'],
           Usuario.termino    : user['termino'],
           Usuario.estado     : user['estado'],
           Usuario.codigo     : user['codigo']})
    db.session.commit()
    return {'response': 'OK', 'message': str(resp) + ' Usuario actualizado', 'data': user}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al modificar el usuario: ' + user['id_usuario']}

def updateUserPassword(user):
  '''
     updateUserPassword: Actualiza la contraseña de un usuario en la colección de usaurio \n
     @params:
        user: objeto Json con los datos de usuario para modificar en la DB, sólo toma _'id', 'id_usuario', 'clave' y 'nueva_clave' 
  '''
  print("In updateUserPassword:", user['id_usuario'])
  try:
    verifica = validatePassword({'id_usuario': user['id_usuario'], 'clave': user['clave']})
    if  verifica['response'] == 'OK':
      nuevaClave = str(user['nueva_clave']).encode()
      encripted = bcrypt.hashpw(nuevaClave, bcrypt.gensalt(12))
      user['clave'] = encripted.decode('utf-8')
      resp = Usuario.query.filter(Usuario.id_usuario == user['id_usuario']).update({Usuario.clave : user['clave']})
      db.session.commit()
      return {'response': 'OK', 'message': str(resp) + ' Usuario actualizado'}
    return verifica
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al modificar el usuario: ' + user['id_usuario']}

def updatePasswordByCodigo(user):
  '''
     updatePasswordByCodigo: Actualiza la contraseña de un usuario despues de validar el código \n
     @params: 
        usuario: Objeto Json con los datos ('id_usuario', 'nueva_clave') del usuario para habilitar modificar la contraseña
  '''
  print("In updatePasswordByCodigo")
  try:
    nuevaClave = str(user['nueva_clave']).encode()
    encripted = bcrypt.hashpw(nuevaClave, bcrypt.gensalt(12))
    user['clave'] = encripted.decode('utf-8')
    resp = Usuario.query.filter(Usuario.id_usuario == user['id_usuario']).update({
           Usuario.clave  : user['clave'],
           Usuario.codigo : 0})
    db.session.commit()
    return {'response': 'OK', 'message': 'Usuario actualizado', 'data': user}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al modificar el usuario: ' + user['id_usuario']}

### ELIMINA
def deleteUserById(idUsuario):
  '''
     deleteUserById: Elimina un usuario de la colección \n
     @params: 
       idUsuario: Id del objeto usuario a eliminar en la DB 
  '''
  print("In deleteUserById:", idUsuario)
  try:
    resp = Usuario.query.filter(Usuario.id_usuario == idUsuario).delete(synchronize_session = 'fetch')
    db.session.commit()
    return {'response': 'OK', 'message': 'Usuario borrado'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al eliminar el usuario: ' + str(idUsuario)}
