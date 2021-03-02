'''
   consultor:
      Administra los accesos a datos de los consultores de Venaycia.com 

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
from src.mysqlConnector.consultores import Consultores
from src.model import empresa
from src.model import user
from src import db
import traceback
# Métodos CRUD en las coleeciones diccionario, empresa y frecuencias
### CREA
def asociateCompany(emp, cons):
  '''
     asociateCompany: Asocia una empresa a un consultor \n
     @params: 
       emp: Nit de la empresa a asociar
       cons: id_usuario del consultor a asociar
  '''
  print("In asociateCompany:", emp)
  try:
    valida = isConsultorInCompany(cons, emp)
    if 'data' in valida:
      estado = valida['data']['estado']
      estado = 'Activo' if estado == 'A' else 'Inactivo'
      return {'response': 'ERROR', 'message': 'El consultor se encuentra ' + estado + ' en la empresa ' + emp}  
    veriEmp = empresa.getCompanyByNIT(emp)
    if not 'data' in veriEmp:
      return {'response': 'ERROR', 'message': 'No existe la empresa con el NIT ' + emp}  
    veriCons = user.getUserByUsuario(cons)
    if not 'data' in veriCons:
      return {'response': 'ERROR', 'message': 'No existe el consultor con el Id de usuario ' + cons}
    perfil = veriCons['data']['perfil']
    if perfil != 'consult':
      return {'response': 'ERROR', 'message': 'No se puede asociar el usuario ' + cons + ' a la empresa ' + emp + ' no tiene los privilegios de consultor'}
    c = Consultores(emp, cons, 'A')
    db.session.add(c)
    db.session.commit()
    return {'response': 'OK', 'message': 'Consultor asociado a la empresa '+ emp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al asociar el usuario ' + cons}

### LEE
def getCompaniesConsultor(idCons):
  '''
     getCompaniesConsultor: Busca todas las empresas en DB \n
     @params: 
       cons: id_usuario del consultor a buscar
  '''
  print("In getCompaniesConsultor")
  try:
    usu = user.getUserByUsuario(idCons)
    if not 'data' in usu:
        return usu
    if usu['data']['perfil'] != 'consult':
      return {'response': 'ERROR', 'message': 'El usuario no tiene privilegios de consultor'}
    consultor = usu.toJSON()
    resp = []
    emps = Consultores.query.filter(Consultores.consultor == idCons, Consultores.estado == 'A')
    for e in emps:
      emp = empresa.getCompanyByNIT(e.empresa)
      if 'data' in emp:
        consultor['empresa'] = emp['empresa']
        resp.append(e.toJSON())
    if len(resp) > 0:
      return {'response': 'OK', 'data': resp}
    return {'response': 'ERROR', 'message': 'No se encontraron empresas para el consultor ' + idCons}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar las empresas'}

def isConsultorInCompany(idCons, idEmpr):
  '''
     isConsultorInCompany: Busca si una empresa está asociada a un consultor en la DB \n
     @params: 
       idCons: id_usuario del consultor a buscar
       idEmpr: nit de la empresa cliente
  '''
  print("In isConsultorInCompany")
  try:
    resp = Consultores.query.filter(Consultores.consultor == idCons, Consultores.empresa == idEmpr).first()
    if resp:
      return {'response': 'OK', 'data': resp.toJSON()}
    return {'response': 'ERROR', 'message': 'El consultor no se encuentra asociado a esta empresa'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar las empresas'}

### ACTUALIZA
def removeConsultor(emp, cons):
  '''
     removeConsultor: Asocia una empresa a un consultor \n
     @params: 
       emp: Nit de la empresa a asociar
       cons: id_usuario del consultor a eleminar
  '''
  print("In removeConsultor:", emp)
  try:
    veriEmp = empresa.getCompanyByNIT(emp)
    if not 'data' in veriEmp:
      return {'response': 'ERROR', 'message': 'No existe la empresa con el NIT ' + emp}  
    veriCons = user.getUserByUsuario(cons)
    if not 'data' in veriCons:
      return {'response': 'ERROR', 'message': 'No existe el consultor con el Id de usuario ' + cons}
    c = Consultores.query.filter(Consultores.empresa == emp, Consultores.consultor == cons).update({
                                 Consultores.estado : 'D'})
    db.session.commit()
    return {'response': 'OK', 'message': 'Consultor eliminado de la empresa '+ emp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al asociar el usuario ' + cons}
